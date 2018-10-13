import requests
import dateutil.parser


def formulate_query(query, **kwargs):
    """
    Arguments:
        query (str): the query string
        kwargs: a dictionary of keword arguments to qualify the query

    Returns:
        (str): query string after parsing all the params
    """
    parsed_query = ("?q={}").format(str(query))
    for (opt, val) in kwargs.items() :
        parsed_qualifier = ("+{}:{}").format(opt, val)
        parsed_query += parsed_qualifier

    return parsed_query 


def fetch_data(url, authentication):
    try:
        results = requests.get(url=url,
                               headers=authentication)
        data = results.json()
    except Exception as e:
        print("Problem fetching data")
        print("Details: {}".format(e))

    else:
        items = data['items']
        stats = []        

        for each in items:
            created_at = dateutil.parser.parse(each["created_at"])
            closed_at = dateutil.parser.parse(each["closed_at"])
            time_took = (closed_at - created_at).seconds
            stats.append(time_took/3600)
        return stats


def crunch_stats(stats):
    """
    Arguments:
        stats (list): a list of time difference in hours
    
    """
    cleaned_stats = [i for i in stats if i >= 0.25]
    total_time = sum(cleaned_stats)
    parged_items = len(stats) - len(cleaned_stats)

    average_time = total_time/len(cleaned_stats)

    return {
        'entry_received': len(stats),
        'entry_parged': parged_items,
        'entry_used': len(cleaned_stats),
        'average_time': average_time,
        'time_unit': 'hours'
    }

