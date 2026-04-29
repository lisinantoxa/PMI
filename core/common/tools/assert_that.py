import allure
from assertpy import assert_that as assertpy_that


def assert_that(val, description):
    with allure.step(description):
        return assertpy_that(val, description)
