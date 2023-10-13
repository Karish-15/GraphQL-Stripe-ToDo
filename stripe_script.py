import stripe
stripe.api_key = "sk_test_51O0rdqSAx2prmQegmfQK9gsyHU0ki4XCNbbXEQXZ7pp01VFnhQlSRhnZ0UGZAhLlp49DMOIKfsjJPcRCsnbqXT4q00HMa64fF4"

stripe.Price.create(
    product ="prod_OoUl1nmBJUZOAS", unit_amount = 20, currency = "usd",
)

