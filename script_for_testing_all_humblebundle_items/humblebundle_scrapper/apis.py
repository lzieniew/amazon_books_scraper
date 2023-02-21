from .services import get_and_parse_bundle_info, get_bundles_infos


def get_bundle_info(bundle_absolute_link):
    return get_and_parse_bundle_info(bundle_absolute_link)


def get_bundles():
    return get_bundles_infos()
