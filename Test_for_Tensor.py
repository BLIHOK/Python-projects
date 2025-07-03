import requests
import time
from datetime import datetime, timedelta, timezone
from typing import List


def calculate_delta(
    time_before_request: datetime,
    time_after_request: datetime,
    deltas_list: List[float],
    request_index: int
) -> None:
    time_delta = time_after_request - time_before_request
    delta_seconds = time_delta.total_seconds()
    deltas_list.append(delta_seconds)
    print(f"Delta time: {request_index} {time_delta}")


def data_parse(url: str) -> None:
    """Основная функция для выполнения запросов и расчёта дельт."""
    count_requests = 5
    deltas: List[float] = []
    moscow_utc = 3
    time_offset = timedelta(hours=moscow_utc)
    
    for i in range(count_requests):
        # Время до запроса
        time_before_request = datetime.now(timezone.utc) + time_offset
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Время после получения ответа
            time_after_request = datetime.now(timezone.utc) + time_offset
            
            # Для первого запроса выводим детальную информацию
            if i == 0:
                # Парсим данные
                time_s = data["time"] / 1000
                from_stmp_to_date = datetime.fromtimestamp(time_s, tz=timezone.utc)
                time_zone = data["clocks"]["213"]["name"]
                time_zone_offset = data["clocks"]["213"]["offsetString"]
                moscow_time = from_stmp_to_date + time_offset
                
            
                print("\nRaw response content:")
                print(response.text)
                print(f"\nTime UTC: {from_stmp_to_date}")
                print(f"Time Moscow: {moscow_time}")
                print(f"Time zone: {time_zone}")
                print(f"Time zone offset: {time_zone_offset}\n")
            
            # Вычисляем дельту для всех запросов
            calculate_delta(
                time_before_request=time_before_request,
                time_after_request=time_after_request,
                deltas_list=deltas,
                request_index=i + 1
            )
            
            # Пауза между запросами
            if i < count_requests - 1:
                time.sleep(0.5)
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except KeyError as e:
            print(f"Data parsing error: Missing key {e}")
    
    # Вычисляем среднюю дельту
    if deltas:
        avg_delta = sum(deltas) / len(deltas)
        print("\nDelta's list:", deltas)
        print(f"Average time delta: {avg_delta:.6f}")
    else:
        print("No successful measurements")


def main() -> None:
    """Точка входа в программу."""
    url = 'https://yandex.com/time/sync.json?geo=213'
    data_parse(url)


if __name__ == "__main__":
    main()