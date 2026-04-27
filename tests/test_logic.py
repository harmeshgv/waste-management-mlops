from backend.main import build_route, deduplicate, distance


def test_distance_is_zero_for_same_points():
    assert distance(12.915, 80.229, 12.915, 80.229) == 0


def test_deduplicate_keeps_highest_severity_for_same_coordinates():
    tasks = [
        {"id": 1, "lat": 12.9, "lng": 80.2, "severity": 1, "waste_type": "packed"},
        {"id": 2, "lat": 12.9, "lng": 80.2, "severity": 3, "waste_type": "open_litter"},
        {"id": 3, "lat": 13.0, "lng": 80.3, "severity": 2, "waste_type": "construction-waste"},
    ]

    unique_tasks = deduplicate(tasks)
    unique_by_id = {task["id"] for task in unique_tasks}

    assert len(unique_tasks) == 2
    assert unique_by_id == {2, 3}


def test_build_route_prioritizes_higher_severity_before_distance():
    tasks = [
        {"id": 1, "lat": 12.915, "lng": 80.229, "severity": 1, "waste_type": "packed"},
        {"id": 2, "lat": 13.0418, "lng": 80.2341, "severity": 3, "waste_type": "open_litter"},
        {"id": 3, "lat": 12.918, "lng": 80.192, "severity": 2, "waste_type": "construction-waste"},
    ]

    route = build_route(tasks, start=(12.915, 80.229))

    assert [task["id"] for task in route] == [2, 3, 1]
