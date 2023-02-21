from datetime import timedelta

from bs4 import BeautifulSoup

from .interfaces import download_data

HUMBLEBUNDLE_ADDRESS = 'http://www.humblebundle.com'


def bundles_html_to_json_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('script', id='landingPage-json-data').text


def bundle_info_html_to_json_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('script', id='webpack-bundle-page-data').text


def get_image_from_resolved_paths(resolved_paths):
    image_field_sequence = ['tile_image', 'featured_image', 'preview_image']
    for field_name in image_field_sequence:
        if field_name in resolved_paths.keys() and resolved_paths[field_name] is not None:
            return resolved_paths[field_name]
    some_images = [image for key, image in resolved_paths.items() if resolved_paths.get(key)]
    return some_images[0] if len(some_images) > 0 else None


# usable data struct:
'''
{
    'books':
    [
        {
            'title': 'bundle1',
            'image_url': 'http://..',
            'link': 'books/bundles...'
        },
        ...
    ],
    'games':
        ...,
    'software':
        ...
}
'''
def bundles_data_to_usable_data(raw_bundles):
    bundles = {}
    for bundle_type in raw_bundles['data'].keys():
        bundles[bundle_type.capitalize()] = raw_bundles['data'][bundle_type]['mosaic'][0]['products']
    result = {}
    for bundle_type in bundles.keys():
        result[bundle_type] = []
        for bundle in bundles[bundle_type]:
            result[bundle_type].append(dict(
                title=bundle['tile_short_name'],
                image_url=bundle['tile_image'],
                link='bundle_info?link=' + bundle['product_url'],
                machine_name=bundle['machine_name']
            ))
    return result


def _add_info_about_tiers_price_differences(result):
    tiers = result['tiers']
    for index, tier in enumerate(tiers):
        if index != 0:
            currency = tier['price'].split(' ')[1]
            current_price = float(tier['price'].split(' ')[0])
            previous_price = float(tiers[index-1]['price'].split(' ')[0])
            tier['price_difference'] = ('%.2f' % (current_price - previous_price)) + ' ' + currency
        else:
            tier['price_difference'] = '0'


# bundle info structure:
'''
{
    bundle_name:
    bundle_url:
    tiers: [
        {
            price='',
            price_difference='',
            items = [{
                image_url='...',
                tier_title='...',
            }]
        }
    ]
}
'''
def bundle_info_to_usable_data(raw_bundle_info):
    result = dict(
        bundle_name=raw_bundle_info['bundleData']['basic_data']['human_name'],
        bundle_url=HUMBLEBUNDLE_ADDRESS + '/' + raw_bundle_info['bundleData']['page_url']
    )
    tiers = []
    only_items = {key: item for key, item in raw_bundle_info['bundleData']['tier_item_data'].items() if 'min_price|money' in item}
    for item_machine_name, item_info in only_items.items():
        price = ('%.2f' % item_info['min_price|money']['amount']) + ' ' + item_info['min_price|money']['currency']
        tier_with_price = [tier for tier in tiers if tier['price'] == price]
        assert len(tier_with_price) <= 1, 'ERROR len of tier_with_price higher than 1!'
        if not tier_with_price:
            tier = dict(price=price, items=[])
            tiers.append(tier)
        else:
            tier = tier_with_price[0]
        image = get_image_from_resolved_paths(item_info['resolved_paths'])
        new_item = dict(
            image_url=image,
            name=item_info['human_name']
        )
        tier['items'].append(new_item)

    result['tiers'] = list(sorted(tiers, key=lambda tier: float(tier['price'].split(' ')[0])))
    _add_info_about_tiers_price_differences(result)
    return result


def get_bundles_infos():
    raw_bundles = download_data(HUMBLEBUNDLE_ADDRESS + '/bundles', parser_func=bundles_html_to_json_data)
    return raw_bundles


def get_and_parse_bundle_info(bundle_relative_link):
    raw_bundle_info = download_data(HUMBLEBUNDLE_ADDRESS + bundle_relative_link, parser_func=bundle_info_html_to_json_data)
    return raw_bundle_info
