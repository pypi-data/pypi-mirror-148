from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_primary_product

from hestia_earth.orchestrator.log import logger
from hestia_earth.orchestrator.utils import get_required_model_param, find_term_match

_ALLOW_ALL = 'all'


def _lookup_values(term: dict, column: str):
    term_id = term.get('@id')
    term_type = term.get('termType')
    lookup = download_lookup(f"{term_type}.csv")
    values = get_table_value(lookup, 'termid', term_id, column_name(column))
    return (values or _ALLOW_ALL).split(';')


def _is_siteType_allowed(_node: dict, data: dict, term_id: str):
    site = data if data.get('@type', data.get('type')) == 'Site' else data.get('site', {})
    site_type = site.get('siteType')
    term = download_hestia(term_id)
    allowed_site_types = _lookup_values(term, 'siteTypesAllowed') if term else [_ALLOW_ALL]
    return True if _ALLOW_ALL in allowed_site_types or not site_type else site_type in allowed_site_types


def _is_primary_product_termType_allowed(_node: dict, data: dict, term_id: str):
    product = find_primary_product(data) or {}
    term_type = product.get('term', {}).get('termType')
    term = download_hestia(term_id)
    allowed_term_types = _lookup_values(term, 'productTermTypesAllowed') if term else [_ALLOW_ALL]
    return True if _ALLOW_ALL in allowed_term_types or not term_type else term_type in allowed_term_types


def _is_primary_product_id_allowed(_node: dict, data: dict, term_id: str):
    product = find_primary_product(data) or {}
    product_term_id = product.get('term', {}).get('@id')
    term = download_hestia(term_id)
    allowed_term_ids = _lookup_values(term, 'productTermIdsAllowed') if term else [_ALLOW_ALL]
    return True if _ALLOW_ALL in allowed_term_ids or not product_term_id else product_term_id in allowed_term_ids


_CHECK_FROM_ARGS = {
    'checkSiteTypeAllowed': _is_siteType_allowed,
    'checkProductTermTypeAllowed': _is_primary_product_termType_allowed,
    'checkProductTermIdAllowed': _is_primary_product_id_allowed
}


def _check_args(node: dict, args: dict, data: dict, term_id: str):
    keys = list(filter(lambda key: key in _CHECK_FROM_ARGS and args[key] is True, args.keys()))
    return len(keys) == 0 or all([_CHECK_FROM_ARGS[key](node, data, term_id) for key in keys])


_RUN_FROM_ARGS = {
    'runNonReliable': lambda node, _data: node.get('reliability', 1) >= 3,
    'runNonAddedTerm': lambda node, _data: 'term' not in node.get('added', []),
    'runNonMeasured': lambda node, _data: node.get('methodTier') != 'measured'
}


def _run_args(node: dict, args: dict, data: dict):
    keys = list(filter(lambda key: key in _RUN_FROM_ARGS and args[key] is True, args.keys()))
    return len(keys) > 0 and all([_RUN_FROM_ARGS[key](node, data) for key in keys])


def _is_empty(node: dict, skip_empty_value: bool = False):
    return node is None or all([
        not skip_empty_value,
        node.get('value') is None or node.get('value') == []
    ])


def should_run(data: dict, model: dict):
    key = get_required_model_param(model, 'key')
    term_id = get_required_model_param(model, 'value')
    args = model.get('runArgs', {})
    node = find_term_match(data.get(key, []), term_id, None)
    # run if: value is empty or force run from args, and all the checks are valid
    run = (
        _is_empty(node, args.get('skipEmptyValue', False)) or _run_args(node, args, data)
    ) and _check_args(node, args, data, term_id)
    logger.info('model=%s, key=%s, value=%s, term=%s, should_run=%s', model.get('model'), key, term_id, term_id, run)
    return run
