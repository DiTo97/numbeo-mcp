"""Tests for the Numbeo SDK client."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pytest

from numbeo_sdk import Numbeo, modeling


@dataclass(slots=True)
class EndpointCase:
    """Represents a single API endpoint interaction for testing."""

    name: str
    method: str
    request: modeling.RequestModel | None
    endpoint: str
    params: dict[str, Any]
    response: Any
    response_model: type[Any]


class MockResponse:
    """HTTPX-like response wrapper returning static JSON payloads."""

    def __init__(self, payload: Any) -> None:
        self._payload = payload

    def json(self) -> Any:
        return self._payload

    def raise_for_status(self) -> None:
        return None


class MockAsyncClient:
    """Minimal async client to capture outgoing calls."""

    def __init__(self, case: EndpointCase) -> None:
        self.case = case
        self.closed = False

    async def get(self, url: str, params: dict[str, Any]) -> MockResponse:
        assert url == f"{Numbeo.URL}/{self.case.endpoint}"
        assert params["api_key"] == "test-key"
        delivered = {key: value for key, value in params.items() if key != "api_key"}
        assert delivered == self.case.params
        return MockResponse(self.case.response)

    async def aclose(self) -> None:
        self.closed = True


ENDPOINT_CASES = [
    EndpointCase(
        name="cities",
        method="get_cities",
        request=None,
        endpoint="cities",
        params={},
        response=json.loads(
            """{
                "cities": [
                    {
                        "country": "Brazil",
                        "city": "Sao Paulo",
                        "latitude": -23.5503279,
                        "city_id": 7392,
                        "longitude": -46.6339647
                    },
                    {
                        "country": "United Kingdom",
                        "city": "London",
                        "latitude": 51.5072759,
                        "city_id": 6512,
                        "longitude": -0.1276597
                    },
                    {
                        "country": "Australia",
                        "city": "Sydney",
                        "latitude": -33.8674869,
                        "city_id": 3581,
                        "longitude": 151.2069902
                    }
                ]
            }"""
        ),
        response_model=modeling.GetCitiesResponse,
    ),
    EndpointCase(
        name="items",
        method="get_items",
        request=modeling.GetItemsRequest(),
        endpoint="items",
        params={},
        response=json.loads(
            """{
                "items": [
                    {
                        "category": "Restaurants",
                        "cpi_factor": 6,
                        "item_id": 3,
                        "name": "McMeal at McDonalds (or Equivalent Combo Meal)",
                        "rent_factor": 0
                    },
                    {
                        "category": "Restaurants",
                        "cpi_factor": 5,
                        "item_id": 4,
                        "name": "Domestic Beer (0.5 liter draught)",
                        "rent_factor": 0
                    },
                    {
                        "category": "Markets",
                        "cpi_factor": 31,
                        "item_id": 9,
                        "name": "Loaf of Fresh White Bread (500g)",
                        "rent_factor": 0
                    },
                    {
                        "category": "Markets",
                        "cpi_factor": 28,
                        "item_id": 11,
                        "name": "Eggs (12)",
                        "rent_factor": 0
                    }
                ]
            }"""
        ),
        response_model=modeling.GetItemsResponse,
    ),
    EndpointCase(
        name="currency_exchange_rates",
        method="get_currency_exchange_rates",
        request=modeling.GetCurrencyExchangeRatesRequest(),
        endpoint="currency_exchange_rates",
        params={},
        response=json.loads(
            """{
                "exchange_rates": [
                    {
                        "one_usd_to_currency": 3.6731000000000003,
                        "one_eur_to_currency": 4.375342465753425,
                        "currency": "AED"
                    },
                    {
                        "one_usd_to_currency": 1.2390999999999999,
                        "one_eur_to_currency": 1.4759976176295413,
                        "currency": "AUD"
                    },
                    {
                        "one_usd_to_currency": 6.2471,
                        "one_eur_to_currency": 7.4414532459797496,
                        "currency": "DKK"
                    }
                ]
            }"""
        ),
        response_model=modeling.GetCurrencyExchangeRatesResponse,
    ),
    EndpointCase(
        name="city_prices",
        method="get_city_prices",
        request=modeling.GetCityPricesRequest(query="London, United Kingdom"),
        endpoint="city_prices",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "name": "London, United Kingdom",
                "currency": "GBP",
                "contributors12months": 943,
                "monthLastUpdate": 4,
                "contributors": 564,
                "yearLastUpdate": 2022,
                "prices": [
                    {
                        "data_points": 82,
                        "item_id": 1,
                        "lowest_price": 10,
                        "average_price": 15,
                        "highest_price": 30,
                        "item_name": "Meal, Inexpensive Restaurant, Restaurants"
                    },
                    {
                        "data_points": 69,
                        "item_id": 5,
                        "lowest_price": 4,
                        "average_price": 5,
                        "highest_price": 7,
                        "item_name": "Imported Beer (0.33 liter bottle), Restaurants"
                    },
                    {
                        "data_points": 71,
                        "item_id": 11,
                        "lowest_price": 1.2344128765489017,
                        "average_price": 2.2980851064307743,
                        "highest_price": 3.600000000144,
                        "item_name": "Eggs (regular) (12), Markets"
                    }
                ],
                "city_id": 6512
            }"""
        ),
        response_model=modeling.GetCityPricesResponse,
    ),
    EndpointCase(
        name="country_prices",
        method="get_country_prices",
        request=modeling.GetCountryPricesRequest(country="Kuwait"),
        endpoint="country_prices",
        params={"country": "Kuwait"},
        response=json.loads(
            """{
                "monthLastUpdate": 4,
                "contributors": 45,
                "name": "Kuwait",
                "prices": [
                    {
                        "average_price": 6.061485913570016,
                        "item_name": "Meal, Inexpensive Restaurant, Restaurants",
                        "highest_price": 13,
                        "item_id": 1,
                        "lowest_price": 3.36080278998022,
                        "data_points": 40
                    },
                    {
                        "average_price": 1.3874939824286925,
                        "item_name": "Oranges (1 kg), Markets",
                        "highest_price": 1.5,
                        "item_id": 111,
                        "lowest_price": 1.25,
                        "data_points": 40
                    },
                    {
                        "average_price": 1.3975,
                        "item_name": "Potato (1 kg), Markets",
                        "highest_price": 1.79,
                        "item_id": 112,
                        "lowest_price": 0.8,
                        "data_points": 22
                    },
                    {
                        "average_price": 2.0949999999999998,
                        "item_name": "Lettuce (1 head), Markets",
                        "highest_price": 3.5,
                        "item_id": 113,
                        "lowest_price": 0.89,
                        "data_points": 25
                    },
                    {
                        "average_price": 3.71844212292207,
                        "item_name": "Cappuccino (regular), Restaurants",
                        "highest_price": 7,
                        "item_id": 114,
                        "lowest_price": 1.97376849168828,
                        "data_points": 40
                    }
                ],
                "yearLastUpdate": 2012,
                "currency": "USD"
            }"""
        ),
        response_model=modeling.GetCountryPricesResponse,
    ),
    EndpointCase(
        name="city_cost_estimator",
        method="get_city_cost_estimator",
        request=modeling.GetCityCostEstimatorRequest(
            query="London, United Kingdom",
            household_members=4,
            children=2,
            include_rent=True,
            currency="USD",
        ),
        endpoint="city_cost_estimator",
        params={
            "query": "London, United Kingdom",
            "members": 4,
            "children": 2,
            "include_rent": True,
            "currency": "USD",
        },
        response=json.loads(
            """{
                "city_name": "London, United Kingdom",
                "household_members": 4,
                "children": 2,
                "currency": "USD",
                "overall_estimate": 11745.345860115707,
                "city_id": 6512,
                "breakdown": [
                    {
                        "estimate": 851.7582208104193,
                        "category": "Restaurants"
                    },
                    {
                        "estimate": 204.69409995334127,
                        "category": "Going out"
                    },
                    {
                        "estimate": 978.8876853696561,
                        "category": "Food at Home"
                    },
                    {
                        "estimate": 65.26440238073204,
                        "category": "Drinks at Home"
                    },
                    {
                        "estimate": 738.5319384894608,
                        "category": "Public Transport and Taxi"
                    },
                    {
                        "estimate": 263.2046891311094,
                        "category": "Leisure and Sport Memberships"
                    },
                    {
                        "estimate": 368.6369360079844,
                        "category": "Utilities"
                    },
                    {
                        "estimate": 134.3677037793451,
                        "category": "Clothing and Shoes"
                    },
                    {
                        "estimate": 4180.452797310392,
                        "category": "Rent"
                    },
                    {
                        "estimate": 3688.0066324803743,
                        "category": "Childcare and School Fees"
                    },
                    {
                        "estimate": 271.5407544028932,
                        "category": "Other Goods and Services"
                    }
                ]
            }"""
        ),
        response_model=modeling.GetCityCostEstimatorResponse,
    ),
    EndpointCase(
        name="close_cities_with_prices",
        method="get_close_cities_with_prices",
        request=modeling.GetCloseCitiesWithPricesRequest(
            query="-12.40,130.8", min_contributors=2, max_distance=10000
        ),
        endpoint="close_cities_with_prices",
        params={
            "query": "-12.40,130.8",
            "min_contributors": 2,
            "max_distance": 10000,
        },
        response=json.loads(
            """{
                "cities": [
                    {
                        "country": "Australia",
                        "latitude": -12.461334,
                        "name": "Darwin",
                        "short_name": "Darwin",
                        "city_id": 3570,
                        "longitude": 130.841904
                    },
                    {
                        "country": "Timor-Leste",
                        "latitude": -8.5536809,
                        "name": "Dili",
                        "short_name": "Dili",
                        "city_id": 4836,
                        "longitude": 125.5784093
                    },
                    {
                        "country": "Australia",
                        "latitude": -23.7002104,
                        "name": "Alice Springs",
                        "short_name": "Alice Springs",
                        "city_id": 8304,
                        "longitude": 133.8806114
                    },
                    {
                        "country": "Indonesia",
                        "latitude": -3.03638,
                        "name": "Jayapura",
                        "short_name": "Jayapura",
                        "city_id": 4079,
                        "longitude": 139.925791727673
                    },
                    {
                        "country": "Indonesia",
                        "latitude": -5.1342962,
                        "name": "Makassar",
                        "short_name": "Makassar",
                        "city_id": 4082,
                        "longitude": 119.4124282
                    },
                    {
                        "country": "Indonesia",
                        "latitude": -8.581824,
                        "name": "Mataram",
                        "short_name": "Mataram",
                        "city_id": 4084,
                        "longitude": 116.106832
                    },
                    {
                        "country": "Indonesia",
                        "latitude": 1.4708889,
                        "name": "Manado",
                        "short_name": "Manado",
                        "city_id": 7869,
                        "longitude": 124.8454608
                    },
                    {
                        "country": "Australia",
                        "latitude": -16.923978,
                        "name": "Cairns",
                        "short_name": "Cairns",
                        "city_id": 3567,
                        "longitude": 145.77086
                    }
                ]
            }"""
        ),
        response_model=modeling.GetCloseCitiesWithPricesResponse,
    ),
    EndpointCase(
        name="country_administrative_units",
        method="get_country_administrative_units",
        request=modeling.GetCountryAdministrativeUnitsRequest(country="Canada"),
        endpoint="country_administrative_units",
        params={"country": "Canada"},
        response=json.loads(
            """[
                "Alberta",
                "British Columbia",
                "Manitoba",
                "New Brunswick / Nouveau-Brunswick",
                "Newfoundland and Labrador",
                "Northwest Territories",
                "Nova Scotia",
                "Ontario",
                "Prince Edward Island",
                "Qu\u00e9bec",
                "Saskatchewan",
                "Yukon",
                "Nunavut"
            ]"""
        ),
        response_model=modeling.GetCountryAdministrativeUnitsResponse,
    ),
    EndpointCase(
        name="administrative_unit_prices_administrative_unit",
        method="get_administrative_unit_prices",
        request=modeling.GetAdministrativeUnitPricesRequest(
            country="United States", administrative_unit="California"
        ),
        endpoint="administrative_unit_prices",
        params={"country": "United States", "administrative_unit": "California"},
        response=json.loads(
            """{
                "monthLastUpdate": 4,
                "contributors": 45,
                "name": "California",
                "prices": [
                    {
                        "average_price": 6.061485913570016,
                        "item_name": "Meal, Inexpensive Restaurant, Restaurants",
                        "highest_price": 13,
                        "item_id": 1,
                        "lowest_price": 3.36080278998022,
                        "data_points": 40
                    },
                    {
                        "average_price": 1.3874939824286925,
                        "item_name": "Oranges (1 kg), Markets",
                        "highest_price": 1.5,
                        "item_id": 111,
                        "lowest_price": 1.25,
                        "data_points": 40
                    },
                    {
                        "average_price": 1.3975,
                        "item_name": "Potato (1 kg), Markets",
                        "highest_price": 1.79,
                        "item_id": 112,
                        "lowest_price": 0.8,
                        "data_points": 22
                    },
                    {
                        "average_price": 2.0949999999999998,
                        "item_name": "Lettuce (1 head), Markets",
                        "highest_price": 3.5,
                        "item_id": 113,
                        "lowest_price": 0.89,
                        "data_points": 25
                    },
                    {
                        "average_price": 3.71844212292207,
                        "item_name": "Cappuccino (regular), Restaurants",
                        "highest_price": 7,
                        "item_id": 114,
                        "lowest_price": 1.97376849168828,
                        "data_points": 40
                    }
                ],
                "yearLastUpdate": 2022,
                "currency": "USD"
            }"""
        ),
        response_model=modeling.GetAdministrativeUnitPricesResponse,
    ),
    EndpointCase(
        name="administrative_unit_prices_admin_name",
        method="get_administrative_unit_prices",
        request=modeling.GetAdministrativeUnitPricesRequest(
            country="Canada", admin_name="Ontario"
        ),
        endpoint="administrative_unit_prices",
        params={"country": "Canada", "admin_name": "Ontario"},
        response=json.loads(
            """{
                "monthLastUpdate": 4,
                "contributors": 45,
                "name": "Ontario",
                "prices": [
                    {
                        "average_price": 6.061485913570016,
                        "item_name": "Meal, Inexpensive Restaurant, Restaurants",
                        "highest_price": 13,
                        "item_id": 1,
                        "lowest_price": 3.36080278998022,
                        "data_points": 40
                    }
                ],
                "yearLastUpdate": 2012,
                "currency": "CAD"
            }"""
        ),
        response_model=modeling.GetAdministrativeUnitPricesResponse,
    ),
    EndpointCase(
        name="historical_city_prices",
        method="get_historical_city_prices",
        request=modeling.GetHistoricalCityPricesRequest(query="London, United Kingdom"),
        endpoint="historical_city_prices",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "entry": [
                    {
                        "amount": 10.4,
                        "year": 2010,
                        "item_id": 1
                    }
                ],
                "city": "London, United Kingdom",
                "currency": "GBP"
            }"""
        ),
        response_model=modeling.GetHistoricalCityPricesResponse,
    ),
    EndpointCase(
        name="historical_country_prices",
        method="get_historical_country_prices",
        request=modeling.GetHistoricalCountryPricesRequest(country="United Kingdom"),
        endpoint="historical_country_prices",
        params={"country": "United Kingdom"},
        response=json.loads(
            """{
                "entry": [
                    {
                        "amount": 630.1988400994201,
                        "item_id": 1,
                        "year": 2010
                    }
                ],
                "currency": "GBP",
                "country": "United Kingdom"
            }"""
        ),
        response_model=modeling.GetHistoricalCountryPricesResponse,
    ),
    EndpointCase(
        name="historical_country_prices_monthly",
        method="get_historical_country_prices_monthly",
        request=modeling.GetHistoricalCountryPricesMonthlyRequest(country="United Kingdom"),
        endpoint="historical_country_prices_monthly",
        params={"country": "United Kingdom"},
        response=json.loads(
            """{
                "entry": [
                    {
                        "amount": 361.95817904595947,
                        "item_id": 1,
                        "year": 2012,
                        "currency": "GBP",
                        "month": 1,
                        "contributors": 13
                    }
                ],
                "country": "United Kingdom"
            }"""
        ),
        response_model=modeling.GetHistoricalCountryPricesMonthlyResponse,
    ),
    EndpointCase(
        name="historical_currency_exchange_rates",
        method="get_historical_currency_exchange_rates",
        request=modeling.GetHistoricalCurrencyExchangeRatesRequest(month=3, year=2014),
        endpoint="historical_currency_exchange_rates",
        params={"month": 3, "year": 2014},
        response=json.loads(
            """{
                "month": 2,
                "year": 2013,
                "exchange_rates": [
                    {
                        "one_usd_to_currency": 0.2722495984318423,
                        "one_eur_to_currency": 0.2014647028395633,
                        "currency": "AED"
                    }
                ]
            }"""
        ),
        response_model=modeling.GetHistoricalCurrencyExchangeRatesResponse,
    ),
    EndpointCase(
        name="indices",
        method="get_indices",
        request=modeling.GetIndicesRequest(query="London, United Kingdom"),
        endpoint="indices",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "crime_index": 53.34230941855818,
                "cpi_and_rent_index": 72.07527649109899,
                "purchasing_power_incl_rent_index": 80.67989242778127,
                "property_price_to_income_ratio": 16.705588892782238,
                "contributors_healthcare": 359,
                "safety_index": 46.65769058144182,
                "traffic_co2_index": 1869.8414096916301,
                "traffic_inefficiency_index": 189.4021258120608,
                "contributors_traffic": 241,
                "rent_index": 65.21959376191104,
                "health_care_index": 70.75969570552323,
                "groceries_index": 58.43652054116736,
                "contributors_property": 98,
                "pollution_index": 58.27208464176413,
                "traffic_time_index": 43.95594713656387,
                "restaurant_price_index": 76.89401514383184,
                "contributors_cost_of_living": 564,
                "climate_index": 88.25433798690545,
                "cpi_index": 78.33661180190455,
                "quality_of_life_index": 127.95751313724718,
                "contributors_pollution": 370,
                "contributors_crime": 1027,
                "traffic_index": 155.89160368069412,
                "name": "London, United Kingdom",
                "city_id": 6512
            }"""
        ),
        response_model=modeling.GetIndicesResponse,
    ),
    EndpointCase(
        name="country_indices",
        method="get_country_indices",
        request=modeling.GetCountryIndicesRequest(country="Kuwait"),
        endpoint="country_indices",
        params={"country": "Kuwait"},
        response=json.loads(
            """{
                "health_care_index": 66.75925925925927,
                "crime_index": 38.84500915750915,
                "traffic_time_index": 17,
                "purchasing_power_incl_rent_index": 104.48707062276117,
                "cpi_index": 77.32543080858119,
                "pollution_index": 69.3103448275862,
                "traffic_index": 93.60606499265447,
                "quality_of_life_index": 141.4787210994602,
                "cpi_and_rent_index": 58.15013366824719,
                "groceries_index": 71.8735218572076,
                "safety_index": 61.154990842490825,
                "name": "Kuwait",
                "rent_index": 37.49969632054832,
                "traffic_co2_index": 4256,
                "restaurant_price_index": 75.45173244741275,
                "traffic_inefficiency_index": 52.48906353257302,
                "property_price_to_income_ratio": 6.989395647748136
            }"""
        ),
        response_model=modeling.GetCountryIndicesResponse,
    ),
    EndpointCase(
        name="city_crime",
        method="get_city_crime",
        request=modeling.GetCityCrimeRequest(query="London, United Kingdom"),
        endpoint="city_crime",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "worried_things_car_stolen": -0.07692307692307693,
                "crime_increasing": 0.45454545454545453,
                "safe_alone_night": 0.6666666666666666,
                "worried_mugged_robbed": -0.8484848484848485,
                "worried_insulted": -0.47692307692307695,
                "problem_violent_crimes": -0.6307692307692307,
                "index_crime": 41.098111957486964,
                "contributors": 69,
                "monthLastUpdate": 3,
                "level_of_crime": -0.5606060606060606
            }"""
        ),
        response_model=modeling.GetCityCrimeResponse,
    ),
    EndpointCase(
        name="city_healthcare",
        method="get_city_healthcare",
        request=modeling.GetCityHealthcareRequest(query="London, United Kingdom"),
        endpoint="city_healthcare",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "location": 0.75,
                "speed": 0.15,
                "modern_equipment": 0.7368421052631579,
                "accuracy_and_completeness": 0.3,
                "cost": 0.45,
                "friendliness_and_courtesy": -0.3684210526315789,
                "responsiveness_waitings": -0.5263157894736842,
                "contributors": 20,
                "city_id": 6189,
                "monthLastUpdate": 2,
                "skill_and_competency": 0.5,
                "insurance_type": {
                    "Employer Sponsored": 10,
                    "None": 5,
                    "Private": 5,
                    "Public": 80
                },
                "name": "London, United Kingdom",
                "index_healthcare": 56.78362573099415,
                "yearLastUpdate": 2015
            }"""
        ),
        response_model=modeling.GetCityHealthcareResponse,
    ),
    EndpointCase(
        name="city_pollution",
        method="get_city_pollution",
        request=modeling.GetCityPollutionRequest(query="London, United Kingdom"),
        endpoint="city_pollution",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "green_and_parks_quality": 1.2062146892655368,
                "pm2.5": 12,
                "comfortable_to_spend_time": 0.19220055710306408,
                "pm10": 23,
                "air_quality": -0.5388888888888889,
                "garbage_disposal_satisfaction": 0.335243553008596,
                "index_pollution": 58.27208464176413,
                "drinking_water_quality_accessibility": 0.7301136363636364,
                "name": "London, United Kingdom",
                "monthLastUpdate": 4,
                "clean_and_tidy": 0.056338028169014086,
                "noise_and_light_pollution": 0.2,
                "contributors": 370,
                "yearLastUpdate": 2022,
                "water_pollution": -0.3659942363112392,
                "city_id": 6512
            }"""
        ),
        response_model=modeling.GetCityPollutionResponse,
    ),
    EndpointCase(
        name="city_traffic",
        method="get_city_traffic",
        request=modeling.GetCityTrafficRequest(query="London, United Kingdom"),
        endpoint="city_traffic",
        params={"query": "London, United Kingdom"},
        response=json.loads(
            """{
                "analyze using Motorbike": {
                    "time_waiting": 0,
                    "time_driving": 0,
                    "time_tram": 0,
                    "time_other": 0,
                    "distance": 10.0584,
                    "time_bike": 0,
                    "time_train": 0,
                    "time_motorbike": 35,
                    "time_walking": 0.75,
                    "count": 4,
                    "time_bus": 0
                }
            }"""
        ),
        response_model=modeling.GetCityTrafficResponse,
    ),
    EndpointCase(
        name="country_crime",
        method="get_country_crime",
        request=modeling.GetCountryCrimeRequest(country="Poland"),
        endpoint="country_crime",
        params={"country": "Poland"},
        response=json.loads(
            """{
                "worried_things_car_stolen": -0.36507936507936506,
                "contributors": 198,
                "crime_increasing": -0.5263157894736842,
                "safe_alone_night": 0.3299492385786802,
                "worried_mugged_robbed": -0.734375,
                "worried_insulted": -0.7157894736842105,
                "problem_violent_crimes": -1.2135416666666667,
                "index_crime": 31.771885317818157,
                "monthLastUpdate": 3,
                "level_of_crime": -0.8115183246073299,
                "worried_skin_ethnic_religion": -0.9947916666666666,
                "problem_drugs": -1.036649214659686,
                "name": "Poland",
                "safe_alone_daylight": 1.5606060606060606,
                "problem_corruption_bribery": -0.1638418079096045,
                "problem_property_crimes": -0.061855670103092786,
                "worried_home_broken": -0.9119170984455959,
                "worried_attacked": -0.6335078534031413,
                "worried_car_stolen": -0.7947368421052632,
                "index_safety": 68.22811468218183,
                "yearLastUpdate": 2015
            }"""
        ),
        response_model=modeling.GetCountryCrimeResponse,
    ),
    EndpointCase(
        name="country_healthcare",
        method="get_country_healthcare",
        request=modeling.GetCountryHealthcareRequest(country="Poland"),
        endpoint="country_healthcare",
        params={"country": "Poland"},
        response=json.loads(
            """{
                "contributors": 78,
                "speed": 0.06493506493506493,
                "location": 0.6842105263157895,
                "modern_equipment": 1.2,
                "accuracy_and_completeness": 0.43243243243243246,
                "cost": 0.38666666666666666,
                "friendliness_and_courtesy": 0.04,
                "responsiveness_waitings": -0.7105263157894737,
                "reportees": 78,
                "monthLastUpdate": 3,
                "skill_and_competency": 0.37662337662337664,
                "insurance_type": {
                    "Employer Sponsored": 21.794871794871796,
                    "None": 1.282051282051282,
                    "Private": 14.102564102564102,
                    "Public": 62.82051282051282
                },
                "name": "Poland",
                "index_healthcare": 57.94724560514035,
                "yearLastUpdate": 2015
            }"""
        ),
        response_model=modeling.GetCountryHealthcareResponse,
    ),
    EndpointCase(
        name="country_pollution",
        method="get_country_pollution",
        request=modeling.GetCountryPollutionRequest(country="Poland"),
        endpoint="country_pollution",
        params={"country": "Poland"},
        response=json.loads(
            """{
                "index_pollution": 49.71328236217564,
                "monthLastUpdate": 3,
                "contributors": 264,
                "noise_and_light_pollution": -0.2765957446808511,
                "garbage_disposal_satisfaction": 0.5473684210526316,
                "drinking_water_quality_accessibility": 0.7604166666666666,
                "water_pollution": -0.6421052631578947,
                "name": "Poland",
                "clean_and_tidy": 0.30526315789473685,
                "air_quality": -0.03435114503816794,
                "comfortable_to_spend_time": 0.2681564245810056,
                "green_and_parks_quality": 0.9361702127659575,
                "yearLastUpdate": 2015
            }"""
        ),
        response_model=modeling.GetCountryPollutionResponse,
    ),
    EndpointCase(
        name="country_traffic",
        method="get_country_traffic",
        request=modeling.GetCountryTrafficRequest(country="Poland"),
        endpoint="country_traffic",
        params={"country": "Poland"},
        response=json.loads(
            """{
                "index_traffic": 116.36304290977134,
                "index_co2_emission": 2750.65,
                "analyze using Bike": {
                    "time_bike": 21.5,
                    "distance": 6.925,
                    "time_bus": 0,
                    "count": 8,
                    "time_waiting": 0,
                    "time_train": 1.875,
                    "time_driving": 0,
                    "time_walking": 0.75,
                    "time_motorbike": 0,
                    "time_other": 0
                },
                "index_time": 33.70625,
                "analyze using Motorbike": {
                    "time_bike": 0,
                    "distance": 7,
                    "time_bus": 0,
                    "count": 1,
                    "time_waiting": 0,
                    "time_train": 0,
                    "time_driving": 0,
                    "time_walking": 0,
                    "time_motorbike": 15,
                    "time_other": 0
                },
                "index_time_exp": 392.4017206429015,
                "analyze using Bus": {
                    "time_bike": 0.8333333333333334,
                    "distance": 9.0875,
                    "time_bus": 25.458333333333332,
                    "count": 24,
                    "time_waiting": 5.854166666666667,
                    "time_train": 1.25,
                    "time_driving": 0.4166666666666667,
                    "time_walking": 8.333333333333334,
                    "time_motorbike": 0.4166666666666667,
                    "time_other": 0.8333333333333334
                },
                "reportees": 93,
                "analyze using Car": {
                    "time_bike": 0,
                    "distance": 14.474074074074075,
                    "time_bus": 0,
                    "count": 27,
                    "time_waiting": 0,
                    "time_train": 0,
                    "time_driving": 24.59259259259259,
                    "time_walking": 2.740740740740741,
                    "time_motorbike": 0,
                    "time_other": 0
                },
                "primary_means_percentage_map": {
                    "Car": 29.347826086956523,
                    "Working from Home": 14.130434782608695,
                    "Train": 9.782608695652174,
                    "Bike": 8.695652173913043,
                    "Walking": 10.869565217391305,
                    "Bus": 26.08695652173913,
                    "Motorbike": 1.0869565217391304
                },
                "name": "Poland",
                "index_inefficiency": 108.1812400671986,
                "analyze using Walking": {
                    "time_bike": 2.8,
                    "distance": 4.13,
                    "time_bus": 2.2,
                    "count": 10,
                    "time_waiting": 1.5,
                    "time_train": 2.7,
                    "time_driving": 0.3,
                    "time_walking": 19.6,
                    "time_motorbike": 0,
                    "time_other": 0
                },
                "overall_average_analyze": {
                    "time_bike": 2.75,
                    "distance": 11.057500000000001,
                    "time_bus": 8.725,
                    "count": 93,
                    "time_waiting": 2.49375,
                    "time_train": 3.8625,
                    "time_driving": 8.525,
                    "time_walking": 6.7,
                    "time_motorbike": 0.3125,
                    "time_other": 0.3375
                },
                "analyze using Train": {
                    "time_bike": 0,
                    "distance": 18.555555555555557,
                    "time_bus": 7.222222222222222,
                    "count": 9,
                    "time_waiting": 4.444444444444445,
                    "time_train": 26,
                    "time_driving": 0.5555555555555556,
                    "time_walking": 6.222222222222222,
                    "time_motorbike": 0,
                    "time_other": 0
                }
            }"""
        ),
        response_model=modeling.GetCountryTrafficResponse,
    ),
    EndpointCase(
        name="rankings_by_city_current",
        method="get_rankings_by_city_current",
        request=modeling.GetRankingsByCityCurrentRequest(section=1),
        endpoint="rankings_by_city_current",
        params={"section": 1},
        response=json.loads(
            """[
                {
                    "country": "Switzerland",
                    "city_name": "Basel",
                    "cpi_and_rent_index": 90.1359163150788,
                    "rent_index": 47.72953844461662,
                    "purchasing_power_incl_rent_index": 135.17535795816121,
                    "restaurant_price_index": 127.7220643349051,
                    "groceries_index": 124.35743301742603,
                    "city_id": 6348,
                    "cpi_index": 128.62588475320365
                }
            ]"""
        ),
        response_model=modeling.GetRankingsByCityCurrentResponse,
    ),
    EndpointCase(
        name="rankings_by_city_historical",
        method="get_rankings_by_city_historical",
        request=modeling.GetRankingsByCityHistoricalRequest(section=1),
        endpoint="rankings_by_city_historical",
        params={"section": 1},
        response=json.loads(
            """{
                "2009": [
                    {
                        "country": "France",
                        "city_name": "Paris",
                        "cpi_and_rent_index": 115.352399333561,
                        "rent_index": 96.3917647058824,
                        "purchasing_power_incl_rent_index": 39.3783859771547,
                        "restaurant_price_index": 116.526933333333,
                        "groceries_index": 117.046356562731,
                        "city_id": 5426,
                        "cpi_index": 127.819456981736
                    }
                ]
            }"""
        ),
        response_model=modeling.GetRankingsByCityHistoricalResponse,
    ),
    EndpointCase(
        name="rankings_by_country_historical",
        method="get_rankings_by_country_historical",
        request=modeling.GetRankingsByCountryHistoricalRequest(section=1),
        endpoint="rankings_by_country_historical",
        params={"section": 1},
        response=json.loads(
            """{
                "2009": [
                    {
                        "country": "Ireland",
                        "cpi_and_rent_index": 110.105298692167,
                        "rent_index": 85.8543137254902,
                        "purchasing_power_incl_rent_index": 59.7959499668058,
                        "restaurant_price_index": 131.562666666667,
                        "groceries_index": 154.514000113591,
                        "cpi_index": 126.050884562128
                    }
                ]
            }"""
        ),
        response_model=modeling.GetRankingsByCountryHistoricalResponse,
    ),
]


def test_client_requires_api_key() -> None:
    """The client must validate that an API key is provided."""

    with pytest.raises(ValueError, match="Numbeo API key is required."):
        Numbeo(key="")


def test_client_stores_key() -> None:
    """Ensure the provided key is exposed via the client attribute."""

    class DummyClient:
        async def aclose(self) -> None:  # pragma: no cover - unused helper
            return None

    dummy_client = DummyClient()
    client = Numbeo(key="abc123", client=dummy_client)
    assert client.key == "abc123"


@pytest.mark.asyncio
async def test_client_context_manager_does_not_close_external_client() -> None:
    """When an external httpx client is supplied it should not be closed automatically."""

    class ExternalClient:
        def __init__(self) -> None:
            self.closed = False

        async def get(self, *_: Any, **__: Any) -> MockResponse:
            return MockResponse({})

        async def aclose(self) -> None:
            self.closed = True

    external = ExternalClient()
    client = Numbeo(key="abc123", client=external)  # type: ignore[arg-type]
    async with client:
        pass
    assert external.closed is False


@pytest.mark.asyncio
@pytest.mark.parametrize("case", ENDPOINT_CASES, ids=[case.name for case in ENDPOINT_CASES])
async def test_endpoint_calls(monkeypatch: pytest.MonkeyPatch, case: EndpointCase) -> None:
    """Verify each client method sends the expected request and parses the response."""

    monkeypatch.setattr(
        "numbeo_sdk.client.httpx.AsyncClient",
        lambda timeout: (  # type: ignore[return-value]
            MockAsyncClient(case) if timeout == 30.0 else None
        ),
    )

    client = Numbeo(key="test-key")

    method = getattr(client, case.method)
    if case.request is None:
        result = await method()
    else:
        result = await method(case.request)

    expected = case.response_model.model_validate(case.response)
    assert result.model_dump() == expected.model_dump()

    await client.close()
