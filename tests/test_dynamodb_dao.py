from app.models import PetStatistics


def test_add_pet(dynamodb_dao):
    dynamodb_dao.add_pet("giraffe")
    response = dynamodb_dao.get_all_pet_events_by_name("giraffe", None)

    assert response == PetStatistics(pet_name="giraffe", count=1)


def test_add_random_pet(dynamodb_table, dynamodb_dao, shared_settings):
    dynamodb_dao.add_random_pet()
    response = dynamodb_dao.get_all_pet_event(None)
    value = 0
    for object in response:
        if object.count == 1:
            value = 1
    assert value == 1
