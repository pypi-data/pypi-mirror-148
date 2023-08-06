#
# Implementation of the Wordpress API for adding / updating / deleting
# events as custom post types. 
#

import requests, warnings

from flask_pluginengine import current_plugin
from requests.auth import HTTPBasicAuth

from indico.modules.events.models.events import EventType

def make_request(method, endpoint, data = {}):
    wp_url = current_plugin.settings.get('wp_url')
    wp_username = current_plugin.settings.get('wp_username')
    wp_password = current_plugin.settings.get('wp_application_password')

    if wp_url[-1] == '/':
        wp_url = wp_url[:-1]
    if endpoint[0] != '/':
        endpoint = '/' + endpoint

    auth = HTTPBasicAuth(wp_username, wp_password)

    if method == 'post':
        response = requests.post(wp_url + endpoint,
            data = data, auth = auth)
    elif method == 'get':
        response = requests.get(wp_url + endpoint,  auth = auth)
    elif method == 'delete':
        response = requests.delete(wp_url + endpoint,  auth = auth)
    else:
        raise RuntimeError('Method not supported: ' % method)
    
    if response.status_code >= 300:
        warnings.warn(response.text)
        raise RuntimeError('Invalid response from the Wordpress API')

    return response

def delete_event(event_id):
    #FIXME: We need support for the indico_id meta and custom
    # event post type to implement this, see update_event(). 
    wp_event = get_event(event_id)

    if wp_event is not None:
        make_request('delete', '/wp-json/wp/v2/unipievents/%d' % wp_event['id'])

def get_event(event_id):
    """Retrieve an event data from Wordpress, if available."""
    response = make_request('get', 'wp-json/wp/v2/unipievents/?externalid=%d' % event_id)
    data = response.json()

    if len(data) > 0:
        return data[0]
    else:
        return None

def get_categories(event):
    """Construct the vector of taxonomies to use in Wordpress"""
    taxonomies = []
    maps = current_plugin.settings.get('wp_category_maps')
    for pair in maps.split(','):
        key, value = map(int, pair.split(":"))
        if key == event.category_id:
            taxonomies.append(value)
    return taxonomies

def update_event(event):
    #FIXME: We need to update this function to post custom post
    # types of type 'event', and to check if an event with the
    # appropriate meta key 'indico_id' exists; if that's the
    # case, we just update the post.

    wp_event = get_event(event.id)

    post_title = event.title

    if event.type == 'lecture':
        description = str(event.description)
    else:
        description = ""
    description += "<p>Further information is available at the <a href=\"%s\">event page</a> on the Indico platform</p>"  % event.external_url

    venue = event.venue_name
    if event.venue_name != "" and event.room_name != "":
        venue = venue + ", "
    venue = venue + event.room_name

    taxonomies = get_categories(event)

    if wp_event:
        # In this case we merge the arrays to make sure 
        # we do not overwrite categories that are set in
        # the wordpress event
        taxonomies = set(taxonomies + wp_event['unipievents_taxonomy'])

    event_data = {
        'status': 'publish',
        'title': post_title,
        'content': description,
        'unipievents_taxonomy': ",".join(map(str, taxonomies)),
        'unipievents_startdate': int(event.start_dt.timestamp()),
        'unipievents_enddate': int(event.end_dt.timestamp()),
        'unipievents_place': event.venue_name,
        'unipievents_externalid': event.id
    }

    endpoint = '/wp-json/wp/v2/unipievents'

    if wp_event is not None:
        endpoint = endpoint + '/%d' % wp_event['id']

    make_request('post', endpoint, event_data)
