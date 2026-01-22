Feature: Search and sort products on Amazon

  Scenario: Search iPhone and sort by price low to high
    Given user is on Amazon homepage
    When user searches for "iPhone 17 Pro Max"
    And user sorts results by low to high price
    Then user should see product names with prices
