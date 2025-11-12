"""Pydantic models describing Numbeo API requests and responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel, model_validator


class RequestModel(BaseModel):
    """Base class for outbound Numbeo API request payloads."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ResponseModel(BaseModel):
    """Base class for Numbeo API responses allowing unknown fields."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class CitySummary(ResponseModel):
    country: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    city_id: int | None = Field(None, alias="city_id")


class GetCitiesRequest(RequestModel):
    country: str | None = None


class GetCitiesResponse(ResponseModel):
    cities: list[CitySummary] = Field(default_factory=list)


class ItemSummary(ResponseModel):
    category: str | None = None
    cpi_factor: float | None = None
    item_id: int | None = Field(None, alias="item_id")
    name: str | None = None
    rent_factor: float | None = None


class GetItemsRequest(RequestModel):
    pass


class GetItemsResponse(ResponseModel):
    items: list[ItemSummary] = Field(default_factory=list)


class CurrencyExchangeRate(ResponseModel):
    one_usd_to_currency: float | None = None
    one_eur_to_currency: float | None = None
    currency: str | None = None


class GetCurrencyExchangeRatesRequest(RequestModel):
    pass


class GetCurrencyExchangeRatesResponse(ResponseModel):
    exchange_rates: list[CurrencyExchangeRate] = Field(default_factory=list)


class PriceEntry(ResponseModel):
    data_points: int | None = None
    item_id: int | None = Field(None, alias="item_id")
    lowest_price: float | None = None
    average_price: float | None = None
    highest_price: float | None = None
    item_name: str | None = None


class GetCityPricesRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None
    currency: str | None = None
    use_estimated: bool | None = None


class GetCityPricesResponse(ResponseModel):
    name: str | None = None
    currency: str | None = None
    contributors_12months: int | None = Field(None, alias="contributors12months")
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    contributors: int | None = None
    year_last_update: int | None = Field(None, alias="yearLastUpdate")
    prices: list[PriceEntry] = Field(default_factory=list)
    city_id: int | None = Field(None, alias="city_id")


class GetCountryPricesRequest(RequestModel):
    country: str
    currency: str | None = None


class GetCountryPricesResponse(ResponseModel):
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    contributors: int | None = None
    name: str | None = None
    prices: list[PriceEntry] = Field(default_factory=list)
    year_last_update: int | None = Field(None, alias="yearLastUpdate")
    currency: str | None = None


class CostEstimatorBreakdown(ResponseModel):
    estimate: float | None = None
    category: str | None = None


class GetCityCostEstimatorRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None
    currency: str | None = None
    household_members: int | None = Field(None, alias="members")
    children: int | None = None
    include_rent: bool | None = None


class GetCityCostEstimatorResponse(ResponseModel):
    city_name: str | None = None
    household_members: int | None = None
    children: int | None = None
    currency: str | None = None
    overall_estimate: float | None = None
    city_id: int | None = Field(None, alias="city_id")
    breakdown: list[CostEstimatorBreakdown] = Field(default_factory=list)


class CloseCitySummary(ResponseModel):
    country: str | None = None
    latitude: float | None = None
    name: str | None = None
    short_name: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    longitude: float | None = None


class GetCloseCitiesWithPricesRequest(RequestModel):
    query: str | None = None
    max_distance: int | None = None
    min_contributors: int | None = None


class GetCloseCitiesWithPricesResponse(ResponseModel):
    cities: list[CloseCitySummary] = Field(default_factory=list)


class GetCountryAdministrativeUnitsRequest(RequestModel):
    country: str


class GetCountryAdministrativeUnitsResponse(RootModel[list[str]]):
    pass


class GetAdministrativeUnitPricesRequest(RequestModel):
    country: str
    administrative_unit: str | None = None
    admin_name: str | None = None
    currency: str | None = None

    @model_validator(mode="after")
    def ensure_unit(self) -> GetAdministrativeUnitPricesRequest:
        if not (self.administrative_unit or self.admin_name):
            msg = "Either administrative_unit or admin_name must be provided."
            raise ValueError(msg)
        return self


class GetAdministrativeUnitPricesResponse(ResponseModel):
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    contributors: int | None = None
    name: str | None = None
    prices: list[PriceEntry] = Field(default_factory=list)
    year_last_update: int | None = Field(None, alias="yearLastUpdate")
    currency: str | None = None


class HistoricalPriceEntry(ResponseModel):
    amount: float | None = None
    year: int | None = None
    item_id: int | None = Field(None, alias="item_id")


class GetHistoricalCityPricesRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None
    currency: str | None = None


class GetHistoricalCityPricesResponse(ResponseModel):
    entry: list[HistoricalPriceEntry] = Field(default_factory=list)
    city: str | None = None
    currency: str | None = None


class HistoricalCountryPriceEntry(ResponseModel):
    amount: float | None = None
    item_id: int | None = Field(None, alias="item_id")
    year: int | None = None


class GetHistoricalCountryPricesRequest(RequestModel):
    country: str
    currency: str | None = None


class GetHistoricalCountryPricesResponse(ResponseModel):
    entry: list[HistoricalCountryPriceEntry] = Field(default_factory=list)
    currency: str | None = None
    country: str | None = None


class HistoricalCountryPriceMonthlyEntry(ResponseModel):
    amount: float | None = None
    item_id: int | None = Field(None, alias="item_id")
    year: int | None = None
    currency: str | None = None
    month: int | None = None
    contributors: int | None = None


class GetHistoricalCountryPricesMonthlyRequest(RequestModel):
    country: str
    currency: str | None = None


class GetHistoricalCountryPricesMonthlyResponse(ResponseModel):
    entry: list[HistoricalCountryPriceMonthlyEntry] = Field(default_factory=list)
    country: str | None = None


class GetHistoricalCurrencyExchangeRatesRequest(RequestModel):
    month: int
    year: int


class GetHistoricalCurrencyExchangeRatesResponse(ResponseModel):
    month: int | None = None
    year: int | None = None
    exchange_rates: list[CurrencyExchangeRate] = Field(default_factory=list)


class GetIndicesRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None


class GetIndicesResponse(ResponseModel):
    crime_index: float | None = None
    cpi_and_rent_index: float | None = None
    purchasing_power_incl_rent_index: float | None = None
    property_price_to_income_ratio: float | None = None
    contributors_healthcare: int | None = None
    safety_index: float | None = None
    traffic_co2_index: float | None = None
    traffic_inefficiency_index: float | None = None
    contributors_traffic: int | None = None
    rent_index: float | None = None
    health_care_index: float | None = None
    groceries_index: float | None = None
    contributors_property: int | None = None
    pollution_index: float | None = None
    traffic_time_index: float | None = None
    restaurant_price_index: float | None = None
    contributors_cost_of_living: int | None = None
    climate_index: float | None = None
    cpi_index: float | None = None
    quality_of_life_index: float | None = None
    contributors_pollution: int | None = None
    contributors_crime: int | None = None
    traffic_index: float | None = None
    name: str | None = None
    city_id: int | None = Field(None, alias="city_id")


class GetCountryIndicesRequest(RequestModel):
    country: str | None = None


class GetCountryIndicesResponse(ResponseModel):
    health_care_index: float | None = None
    crime_index: float | None = None
    traffic_time_index: float | None = None
    purchasing_power_incl_rent_index: float | None = None
    cpi_index: float | None = None
    pollution_index: float | None = None
    traffic_index: float | None = None
    quality_of_life_index: float | None = None
    cpi_and_rent_index: float | None = None
    groceries_index: float | None = None
    safety_index: float | None = None
    name: str | None = None
    rent_index: float | None = None
    traffic_co2_index: float | None = None
    restaurant_price_index: float | None = None
    traffic_inefficiency_index: float | None = None
    property_price_to_income_ratio: float | None = None


class GetCityCrimeRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None


class GetCityCrimeResponse(ResponseModel):
    worried_things_car_stolen: float | None = None
    crime_increasing: float | None = None
    safe_alone_night: float | None = None
    worried_mugged_robbed: float | None = None
    worried_insulted: float | None = None
    problem_violent_crimes: float | None = None
    index_crime: float | None = None
    contributors: int | None = None
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    level_of_crime: float | None = None


class GetCityHealthcareRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None


class GetCityHealthcareResponse(ResponseModel):
    location: float | None = None
    speed: float | None = None
    modern_equipment: float | None = None
    accuracy_and_completeness: float | None = None
    cost: float | None = None
    friendliness_and_courtesy: float | None = None
    responsiveness_waitings: float | None = None
    contributors: int | None = None
    city_id: int | None = Field(None, alias="city_id")
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    skill_and_competency: float | None = None
    insurance_type: dict[str, float | int] | None = None
    name: str | None = None
    index_healthcare: float | None = None
    year_last_update: int | None = Field(None, alias="yearLastUpdate")


class GetCityPollutionRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None


class GetCityPollutionResponse(ResponseModel):
    green_and_parks_quality: float | None = None
    pm2_5: float | None = Field(None, alias="pm2.5")
    comfortable_to_spend_time: float | None = None
    pm10: float | None = None
    air_quality: float | None = None
    garbage_disposal_satisfaction: float | None = None
    index_pollution: float | None = None
    drinking_water_quality_accessibility: float | None = None
    name: str | None = None
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    clean_and_tidy: float | None = None
    noise_and_light_pollution: float | None = None
    contributors: int | None = None
    year_last_update: int | None = Field(None, alias="yearLastUpdate")
    water_pollution: float | None = None
    city_id: int | None = Field(None, alias="city_id")


class CommuteSummary(ResponseModel):
    time_waiting: float | None = None
    time_driving: float | None = None
    time_tram: float | None = None
    time_other: float | None = None
    distance: float | None = None
    time_bike: float | None = None
    time_train: float | None = None
    time_motorbike: float | None = None
    time_walking: float | None = None
    count: float | None = None
    time_bus: float | None = None


class GetCityTrafficRequest(RequestModel):
    query: str | None = None
    city: str | None = None
    country: str | None = None
    city_id: int | None = Field(None, alias="city_id")
    strict_matching: bool | None = None


class GetCityTrafficResponse(ResponseModel):
    analyze_using_motorbike: CommuteSummary | None = Field(None, alias="analyze using Motorbike")
    analyze_using_bike: CommuteSummary | None = Field(None, alias="analyze using Bike")
    analyze_using_bus: CommuteSummary | None = Field(None, alias="analyze using Bus")
    analyze_using_car: CommuteSummary | None = Field(None, alias="analyze using Car")
    analyze_using_train: CommuteSummary | None = Field(None, alias="analyze using Train")
    analyze_using_walking: CommuteSummary | None = Field(None, alias="analyze using Walking")
    overall_average_analyze: CommuteSummary | None = Field(None, alias="overall_average_analyze")
    name: str | None = None
    city_id: int | None = Field(None, alias="city_id")


class GetCountryCrimeRequest(RequestModel):
    country: str | None = None


class GetCountryCrimeResponse(ResponseModel):
    worried_things_car_stolen: float | None = None
    contributors: int | None = None
    crime_increasing: float | None = None
    safe_alone_night: float | None = None
    worried_mugged_robbed: float | None = None
    worried_insulted: float | None = None
    problem_violent_crimes: float | None = None
    index_crime: float | None = None
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    level_of_crime: float | None = None
    worried_skin_ethnic_religion: float | None = None
    problem_drugs: float | None = None
    name: str | None = None
    safe_alone_daylight: float | None = None
    problem_corruption_bribery: float | None = None
    problem_property_crimes: float | None = None
    worried_home_broken: float | None = None
    worried_attacked: float | None = None
    worried_car_stolen: float | None = None
    index_safety: float | None = None
    year_last_update: int | None = Field(None, alias="yearLastUpdate")


class GetCountryHealthcareRequest(RequestModel):
    country: str | None = None


class GetCountryHealthcareResponse(ResponseModel):
    contributors: int | None = None
    speed: float | None = None
    location: float | None = None
    modern_equipment: float | None = None
    accuracy_and_completeness: float | None = None
    cost: float | None = None
    friendliness_and_courtesy: float | None = None
    responsiveness_waitings: float | None = None
    reportees: int | None = None
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    skill_and_competency: float | None = None
    insurance_type: dict[str, float | int] | None = None
    name: str | None = None
    index_healthcare: float | None = None
    year_last_update: int | None = Field(None, alias="yearLastUpdate")


class GetCountryPollutionRequest(RequestModel):
    country: str | None = None


class GetCountryPollutionResponse(ResponseModel):
    index_pollution: float | None = None
    month_last_update: int | None = Field(None, alias="monthLastUpdate")
    contributors: int | None = None
    noise_and_light_pollution: float | None = None
    garbage_disposal_satisfaction: float | None = None
    drinking_water_quality_accessibility: float | None = None
    water_pollution: float | None = None
    name: str | None = None
    clean_and_tidy: float | None = None
    air_quality: float | None = None
    comfortable_to_spend_time: float | None = None
    green_and_parks_quality: float | None = None
    year_last_update: int | None = Field(None, alias="yearLastUpdate")


class CountryCommuteSummary(ResponseModel):
    time_bike: float | None = None
    distance: float | None = None
    time_bus: float | None = None
    count: float | None = None
    time_waiting: float | None = None
    time_train: float | None = None
    time_driving: float | None = None
    time_walking: float | None = None
    time_motorbike: float | None = None
    time_other: float | None = None


class GetCountryTrafficRequest(RequestModel):
    country: str | None = None


class GetCountryTrafficResponse(ResponseModel):
    index_traffic: float | None = None
    index_co2_emission: float | None = None
    analyze_using_bike: CountryCommuteSummary | None = Field(None, alias="analyze using Bike")
    index_time: float | None = None
    analyze_using_motorbike: CountryCommuteSummary | None = Field(None, alias="analyze using Motorbike")
    index_time_exp: float | None = None
    analyze_using_bus: CountryCommuteSummary | None = Field(None, alias="analyze using Bus")
    reportees: int | None = None
    analyze_using_car: CountryCommuteSummary | None = Field(None, alias="analyze using Car")
    primary_means_percentage_map: dict[str, float] | None = None
    name: str | None = None
    index_inefficiency: float | None = None
    analyze_using_walking: CountryCommuteSummary | None = Field(None, alias="analyze using Walking")
    overall_average_analyze: CountryCommuteSummary | None = Field(None, alias="overall_average_analyze")
    analyze_using_train: CountryCommuteSummary | None = Field(None, alias="analyze using Train")


class GetRankingsByCityCurrentRequest(RequestModel):
    section: int


class CityRanking(ResponseModel):
    country: str | None = None
    city_name: str | None = None
    cpi_and_rent_index: float | None = None
    rent_index: float | None = None
    purchasing_power_incl_rent_index: float | None = None
    restaurant_price_index: float | None = None
    groceries_index: float | None = None
    city_id: int | None = Field(None, alias="city_id")
    cpi_index: float | None = None


class GetRankingsByCityCurrentResponse(RootModel[list[CityRanking]]):
    pass


class GetRankingsByCityHistoricalRequest(RequestModel):
    section: int


class GetRankingsByCityHistoricalResponse(RootModel[dict[str, list[CityRanking]]]):
    pass


class GetRankingsByCountryHistoricalRequest(RequestModel):
    section: int


class CountryRanking(ResponseModel):
    country: str | None = None
    cpi_and_rent_index: float | None = None
    rent_index: float | None = None
    purchasing_power_incl_rent_index: float | None = None
    restaurant_price_index: float | None = None
    groceries_index: float | None = None
    cpi_index: float | None = None


class GetRankingsByCountryHistoricalResponse(RootModel[dict[str, list[CountryRanking]]]):
    pass


__all__ = [
    "RequestModel",
    "ResponseModel",
    "CitySummary",
    "GetCitiesRequest",
    "GetCitiesResponse",
    "ItemSummary",
    "GetItemsRequest",
    "GetItemsResponse",
    "CurrencyExchangeRate",
    "GetCurrencyExchangeRatesRequest",
    "GetCurrencyExchangeRatesResponse",
    "PriceEntry",
    "GetCityPricesRequest",
    "GetCityPricesResponse",
    "GetCountryPricesRequest",
    "GetCountryPricesResponse",
    "CostEstimatorBreakdown",
    "GetCityCostEstimatorRequest",
    "GetCityCostEstimatorResponse",
    "CloseCitySummary",
    "GetCloseCitiesWithPricesRequest",
    "GetCloseCitiesWithPricesResponse",
    "GetCountryAdministrativeUnitsRequest",
    "GetCountryAdministrativeUnitsResponse",
    "GetAdministrativeUnitPricesRequest",
    "GetAdministrativeUnitPricesResponse",
    "HistoricalPriceEntry",
    "GetHistoricalCityPricesRequest",
    "GetHistoricalCityPricesResponse",
    "HistoricalCountryPriceEntry",
    "GetHistoricalCountryPricesRequest",
    "GetHistoricalCountryPricesResponse",
    "HistoricalCountryPriceMonthlyEntry",
    "GetHistoricalCountryPricesMonthlyRequest",
    "GetHistoricalCountryPricesMonthlyResponse",
    "GetHistoricalCurrencyExchangeRatesRequest",
    "GetHistoricalCurrencyExchangeRatesResponse",
    "GetIndicesRequest",
    "GetIndicesResponse",
    "GetCountryIndicesRequest",
    "GetCountryIndicesResponse",
    "GetCityCrimeRequest",
    "GetCityCrimeResponse",
    "GetCityHealthcareRequest",
    "GetCityHealthcareResponse",
    "GetCityPollutionRequest",
    "GetCityPollutionResponse",
    "CommuteSummary",
    "GetCityTrafficRequest",
    "GetCityTrafficResponse",
    "GetCountryCrimeRequest",
    "GetCountryCrimeResponse",
    "GetCountryHealthcareRequest",
    "GetCountryHealthcareResponse",
    "GetCountryPollutionRequest",
    "GetCountryPollutionResponse",
    "CountryCommuteSummary",
    "GetCountryTrafficRequest",
    "GetCountryTrafficResponse",
    "GetRankingsByCityCurrentRequest",
    "CityRanking",
    "GetRankingsByCityCurrentResponse",
    "GetRankingsByCityHistoricalRequest",
    "GetRankingsByCityHistoricalResponse",
    "GetRankingsByCountryHistoricalRequest",
    "CountryRanking",
    "GetRankingsByCountryHistoricalResponse",
]
