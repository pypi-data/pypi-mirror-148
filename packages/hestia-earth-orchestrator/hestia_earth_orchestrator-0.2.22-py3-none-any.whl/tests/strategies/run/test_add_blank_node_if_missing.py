from unittest.mock import patch

from hestia_earth.orchestrator.strategies.run.add_blank_node_if_missing import should_run

class_path = 'hestia_earth.orchestrator.strategies.run.add_blank_node_if_missing'
FAKE_EMISSION = {'@id': 'n2OToAirExcretaDirect', 'termType': 'emission'}


@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run(mock_node_exists, *args):
    data = {}
    model = {}

    # node does not exists => run
    mock_node_exists.return_value = None
    assert should_run(data, model) is True

    # node exists but no value => run
    mock_node_exists.return_value = {}
    assert should_run(data, model) is True

    # node exists with value + no params => no run
    node = {'value': 10}
    mock_node_exists.return_value = node
    assert not should_run(data, model)


@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_skipEmptyValue(mock_node_exists, *args):
    data = {}

    # no value and not skip => run
    mock_node_exists.return_value = {}
    model = {'runArgs': {'skipEmptyValue': False}}
    assert should_run(data, model) is True

    # no value and skip => no run
    mock_node_exists.return_value = {}
    model = {'runArgs': {'skipEmptyValue': True}}
    assert not should_run(data, model)


@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_runNonReliable(mock_node_exists, *args):
    data = {}
    node = {'value': 10}
    mock_node_exists.return_value = node
    model = {'runArgs': {'runNonReliable': True}}

    # node is reliable => no run
    node['reliability'] = 2
    assert not should_run(data, model)

    # node is not reliable => run
    node['reliability'] = 3
    assert should_run(data, model) is True


@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_runNonAddedTerm(mock_node_exists, *args):
    data = {}
    node = {'value': 10}
    mock_node_exists.return_value = node
    model = {'runArgs': {'runNonAddedTerm': True}}

    # term has been added => no run
    node['added'] = ['term']
    assert not should_run(data, model)

    # term has not been added => run
    node['added'] = []
    assert should_run(data, model) is True


@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_runNonMeasured(mock_node_exists, *args):
    data = {}
    node = {'value': 10}
    mock_node_exists.return_value = node
    model = {'runArgs': {'runNonMeasured': True}}

    # term measured => no run
    node['methodTier'] = 'measured'
    assert not should_run(data, model)

    # term not measured => run
    node['methodTier'] = 'background'
    assert should_run(data, model) is True


@patch(f"{class_path}.get_table_value", return_value='cropland;lake')
@patch(f"{class_path}.download_hestia", return_value=FAKE_EMISSION)
@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_checkSiteTypeAllowed(mock_node_exists, *args):
    data = {}
    node = {'term': FAKE_EMISSION}
    mock_node_exists.return_value = node
    model = {'runArgs': {'checkSiteTypeAllowed': True}}

    # siteType is not allowed => no run
    data['site'] = {'siteType': 'pond'}
    assert not should_run(data, model)

    # siteType is allowed => run
    data['site'] = {'siteType': 'cropland'}
    assert should_run(data, model) is True


@patch(f"{class_path}.get_table_value", return_value='crop;liveAnimal')
@patch(f"{class_path}.download_hestia", return_value=FAKE_EMISSION)
@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_checkProductTermTypeAllowed(mock_node_exists, *args):
    data = {}
    node = {'term': FAKE_EMISSION}
    mock_node_exists.return_value = node
    model = {'runArgs': {'checkProductTermTypeAllowed': True}}
    product = {'primary': True}
    data['products'] = [product]

    # termType is not allowed => no run
    product['term'] = {'termType': 'animalProduct'}
    assert not should_run(data, model)

    # termType is allowed => run
    product['term'] = {'termType': 'crop'}
    assert should_run(data, model) is True


@patch(f"{class_path}.get_table_value", return_value='wheatGrain;seed')
@patch(f"{class_path}.download_hestia", return_value=FAKE_EMISSION)
@patch(f"{class_path}.get_required_model_param", return_value='')
@patch(f"{class_path}.find_term_match")
def test_should_run_checkProductTermIdAllowed(mock_node_exists, *args):
    data = {}
    node = {'term': FAKE_EMISSION}
    mock_node_exists.return_value = node
    model = {'runArgs': {'checkProductTermIdAllowed': True}}
    product = {'primary': True}
    data['products'] = [product]

    # id is not allowed => no run
    product['term'] = {'@id': 'genericCrop'}
    assert not should_run(data, model)

    # id is allowed => run
    product['term'] = {'@id': 'wheatGrain'}
    assert should_run(data, model) is True
