import requests

API_URL = "http://127.0.0.1:8000"


# запуск теста
def test_root():
    assert requests.get(API_URL).status_code == 404


# проверка несуществующего объявления
def test_get_advertisement_not_exits():
    response = requests.get(f"{API_URL}/advertisements/777")
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "description": "Advertisement not found",
    }


# проверка существующего объявления
def test_get_advertisement_exits(
    create_advertisement,
):  #  create_advertisement - фикстура с conftest.py (импортировать не нужно)
    advertisement_id = create_advertisement[
        "id"
    ]  # получаем id созданного фикстурой объявления
    response = requests.get(
        f"{API_URL}/advertisements/{advertisement_id}"
    )  # получаем объявления
    assert response.status_code == 200
    advertisement = response.json()  # получаем json() полученного объявления
    assert create_advertisement["title"] == advertisement["title"]


# проверка создание объявления
def test_create_advertisement():
    response = requests.post(
        f"{API_URL}/advertisements/",
        json={
            "title": "advertisement1",
            "description": "description1",
            "owner": "owner1",
        },
    )
    assert response.status_code == 200
    advertisement_data = response.json()
    assert "id" in advertisement_data
    assert isinstance(advertisement_data["id"], int)


# проверка создание дубликата объявления
def test_create_duplicate_advertisement():
    response = requests.post(
        f"{API_URL}/advertisements/",
        json={
            "title": "advertisement1",
            "description": "description1",
            "owner": "owner1",
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "status": "error",
        "description": "Advertisement olready exists",
    }


# обновление объявления
def test_patch_advertisement(create_advertisement):
    advertisement_id = create_advertisement[
        "id"
    ]  # получаем id созданного фикстурой объявления
    response = requests.patch(
        f"{API_URL}/advertisements/{advertisement_id}",
        json={"title": "updated_advertisement"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "advertisement {advertisement.title} successfully updated"
    }

    response = requests.get(
        f"{API_URL}/advertisements/{advertisement_id}"
    )  # получаем объявление
    title = response.json()["title"]
    assert response.status_code == 200
    assert title == "updated_advertisement"


# удаление объявления
def test_delete_advertisement(create_advertisement):
    advertisement_id = create_advertisement[
        "id"
    ]  # получаем id созданного фикстурой объявления
    response = requests.delete(f"{API_URL}/advertisements/{advertisement_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "advertisement successfully deleted"}

    response = requests.get(f"{API_URL}/advertisements/{advertisement_id}")
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "description": "Advertisement not found",
    }
