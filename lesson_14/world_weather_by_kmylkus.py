"""Here is a solution using the strategy pattern for aggregation types, we can define aggregation strategies as classes,then create
 instances of these strategies based on the requested aggregation type and use them accordingly.
 It uses a generator to efficiently calculate the aggregated temperature for each city without
 loading all data into memory and heap to find the top N cities efficiently."""
from dataclasses import dataclass
from typing import Set, List
from datetime import date
from statistics import mean, median
import heapq

MIN_POPULATION = 50000

@dataclass
class City:
    id: str
    name: str
    population: int


@dataclass
class DailyTemp:
    date: date
    temperature: float


class WeatherAPI:
    def getAllCitiesByIds(self, city_ids: Set[str]) -> Set[City]:
        # return cities
        pass

    def getLastYearTemperature(self, city_id: str) -> List[DailyTemp]:
        # return daily_temperatures
        pass


# Aggregation strategy interface
class AggregationStrategy:
    def calculate(self, temperatures: List[float]) -> float:
        pass


# Aggregation strategies
class AvgAggregation(AggregationStrategy):
    def calculate(self, temperatures: List[float]) -> float:
        return mean(temperatures)


class MedianAggregation(AggregationStrategy):
    def calculate(self, temperatures: List[float]) -> float:
        return median(temperatures)


class MaxAggregation(AggregationStrategy):
    def calculate(self, temperatures: List[float]) -> float:
        return max(temperatures)


# dictionary to map aggregation types to strategy classes
aggregation_strategies = {
    'avg': AvgAggregation(),
    'median': MedianAggregation(),
    'max': MaxAggregation(),
}


def top_cities_by_aggregation(city_ids: Set[str], aggregation_type: str, N: int) -> List[dict]:
    weather_api = WeatherAPI()
    cities = weather_api.getAllCitiesByIds(city_ids)

    # generator function to yield city and aggregated temperature
    def city_temperatures_generator():
        for city in cities:
            temperature_data = weather_api.getLastYearTemperature(city.id)
            temperatures = [temp.temperature for temp in temperature_data]
            yield city, temperatures

    # get aggregation strategy
    aggregation_strategy = aggregation_strategies.get(aggregation_type)
    if not aggregation_strategy:
        raise ValueError(f"Unsupported aggregation type: {aggregation_type}")

    top_cities_data = []
    for city, temperatures in city_temperatures_generator():
        if city.population > MIN_POPULATION:
            #use heap
            aggregated_temperature = aggregation_strategy.calculate(temperatures)
            if len(top_cities_data) < N:
                heapq.heappush(top_cities_data, (aggregated_temperature, city))
            else:
                heapq.heappushpop(top_cities_data, (aggregated_temperature, city))

    # Save data as collection
    top_cities = [{'City': city.name, 'AggregatedTemperature': aggregated_temperature} for aggregated_temperature, city
                  in sorted(top_cities_data, reverse=True)]

    return top_cities


# Example usage
city_ids = {'TLV', 'NY'}
aggregation_type = 'avg'
N = 40
top_cities = top_cities_by_aggregation(city_ids, aggregation_type, N)

for i, city_data in enumerate(top_cities):
    print(f"{i + 1}. {city_data['City']}: {city_data['AggregatedTemperature']:.2f} {aggregation_type}")
