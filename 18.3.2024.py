import requests
import json

def get_vacancies():
    vacancies = []
    page = 0
    per_page = 100  # Количество вакансий на одной странице

    while True:
        # Задаем параметры поиска
        params = {
            'text': 'Python',
            'area': [1, 2],  # 1 - Москва, 2 - Санкт-Петербург
            'search_field': 'name',
            'only_with_salary': True,
            'currency': 'RUR',
            'specialization': 1,  # Программирование, Разработка
            'page': page,
            'per_page': per_page
        }

        # Отправляем GET-запрос на сайт HeadHunter
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        if response.status_code == 200:
            vacancies_data = response.json()
            items = vacancies_data.get('items', [])
            vacancies.extend(items)
            if len(items) < per_page:
                break  # Выход из цикла, если получены не все вакансии
            else:
                page += 1
        else:
            print("Failed to retrieve vacancies")
            break

    print(f"Total vacancies found: {len(vacancies)}")
    return vacancies

def parse_vacancies(vacancies):
    parsed_vacancies = []
    for vacancy in vacancies:
        title = vacancy.get('name', '').lower()  # Преобразуем заголовок в нижний регистр для удобства сравнения
        if 'django' in title or 'flask' in title:
            parsed_vacancy = {
                'title': title,
                'company': vacancy.get('employer', {}).get('name', ''),
                'city': vacancy.get('area', {}).get('name', ''),
                'salary': vacancy.get('salary', {}),
                'url': vacancy.get('url', '')
            }
            parsed_vacancies.append(parsed_vacancy)
    return parsed_vacancies

def main():
    vacancies = get_vacancies()
    parsed_vacancies = parse_vacancies(vacancies)
    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_vacancies, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
