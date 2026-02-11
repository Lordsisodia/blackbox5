---
{
  "fetch": {
    "url": "https://shopify.dev/api/admin-rest/usage/rate-limits",
    "fetched_at": "2026-02-10T13:39:44.483792",
    "status": 200,
    "size_bytes": 252818
  },
  "metadata": {
    "title": "REST Admin API rate limits",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "usage",
    "component": "rate-limits"
  }
}
---

# REST Admin API rate limits

ExpandOn this page- [Key figures](/docs/api/admin-rest/usage/rate-limits#key-figures)- [The leaky bucket algorithm](/docs/api/admin-rest/usage/rate-limits#the-leaky-bucket-algorithm)- [Rate limits](/docs/api/admin-rest/usage/rate-limits#rate-limits)- [Resource-based rate limits](/docs/api/admin-rest/usage/rate-limits#resource-based-rate-limits)- [Avoiding rate limit errors](/docs/api/admin-rest/usage/rate-limits#avoiding-rate-limit-errors)

# REST Admin API rate limitsAsk assistantLegacyThe REST Admin API is a legacy API as of October 1, 2024. All apps and integrations should be built with the [GraphQL Admin API](/docs/api/admin-graphql). For details and migration steps, visit our [migration guide](/docs/apps/build/graphql/migrate).**Legacy:** The REST Admin API is a legacy API as of October 1, 2024. All apps and integrations should be built with the [GraphQL Admin API](/docs/api/admin-graphql). For details and migration steps, visit our [migration guide](/docs/apps/build/graphql/migrate).To ensure our platform remains stable and fair for everyone, the [REST Admin API](/docs/api/admin-rest) is rate-limited. We use a variety of strategies to enforce rate limits. We ask developers to use [industry standard techniques](#avoiding-rate-limit-errors) for limiting calls, caching results, and re-trying requests responsibly.

## [Anchor to Key figures](/docs/api/admin-rest/usage/rate-limits#key-figures)Key figuresThe following are the key figures for rate limiting in the REST Admin API:

-

**Rate-limiting method**: Apps can make a maximum number of requests per minute. For example, 40 API requests within 60 seconds. Each request counts equally, regardless of how much or how little data is returned.

-

**Standard limit**: 2 requests/second

-

**Advanced Shopify limit**: 4 requests/second

-

**Shopify Plus limit**: 20 requests/second

-

**Shopify for enterprise (Commerce Components)**: 40 requests/ second

Shopify might temporarily reduce API rate limits to protect platform stability. We will strive to keep these instances brief and rare. However, your application should be built to handle limits gracefully.

## [Anchor to The leaky bucket algorithm](/docs/api/admin-rest/usage/rate-limits#the-leaky-bucket-algorithm)The leaky bucket algorithmAll Shopify APIs use a [leaky bucket algorithm](https://en.wikipedia.org/wiki/Leaky_bucket) to manage requests. The main points to understand about the leaky bucket metaphor are as follows:

-

Each app has access to a bucket. It can hold, say, 60 “marbles”.

-

Each API request tosses [some number](#key-figures) of marbles into the bucket.

-

Each second, a marble is removed from the bucket (if there are any). This restores capacity for more marbles.

-

If the bucket gets full, you get a throttle error and have to wait for more bucket capacity to become available.

This model ensures that apps that manage API calls responsibly can maintain capacity to make bursts of requests when needed. For example, if you average 20 requests (“marbles”) per second but suddenly need to make 30 requests all at once, you can still do so without hitting your rate limit.

The basic principles of the leaky bucket algorithm apply to all our rate limits, regardless of the specific [methods](/docs/api/usage/limits#rate-limiting-methods) used to apply them.

## [Anchor to Rate limits](/docs/api/admin-rest/usage/rate-limits#rate-limits)Rate limitsCalls to the REST Admin API are governed by request-based limits, which means you should consider the total number of API calls your app makes. In addition, there are resource-based rate limits and throttles.REST Admin API rate limits are based on the combination of the app and store. This means that calls from one app don't affect the rate limits of another app, even on the same store. Similarly, calls to one store don't affect the rate limits of another store, even from the same app.Limits are calculated using the leaky bucket algorithm. All requests that are made after rate limits have been exceeded are throttled and an HTTP `429 Too Many Requests` error is returned. Requests succeed again after enough requests have emptied out of the bucket. You can see the current state of the throttle for a store by using the rate limits header.The *bucket size* and *leak rate* properties determine the API’s burst behavior and request rate.The default settings are as follows:

-

**Bucket size**: `40 requests/app/store`

-

**Leak rate**: `2/second`

PlusThe bucket size and leak rate is increased by a factor of 10 for [Shopify Plus stores](https://www.shopify.com/plus):

**Bucket size**: `400 requests/app/store`

- **Leak rate**: `20/second`

**Plus:** The bucket size and leak rate is increased by a factor of 10 for [Shopify Plus stores](https://www.shopify.com/plus):

- **Bucket size**: `400 requests/app/store`

- **Leak rate**: `20/second`

If the bucket size is exceeded, then an HTTP `429 Too Many Requests` error is returned. The bucket empties at a leak rate of two requests per second. To avoid being throttled, you can build your app to average two requests per second. The throttle is a pass or fail operation. If there is available capacity in your bucket, then the request is executed without queueing or processing delays. Otherwise, the request is throttled.

There is an additional rate limit for GET requests. When the value of the `page` parameter results in an offset of over 100,000 of the requested resource, a `429 Too Many Requests` error is returned. For example, a request to `GET /admin/collects.json?limit=250&page=401` would generate an offset of 100,250 (250 x 401 = 100,250) and return a 429 response.

CautionPage-based pagination was deprecated in the REST Admin API with version 2019-07. Use [cursor-based pagination](/docs/api/usage/pagination-rest) instead.**Caution:** Page-based pagination was deprecated in the REST Admin API with version 2019-07. Use [cursor-based pagination](/docs/api/usage/pagination-rest) instead.

### [Anchor to Rate limits header](/docs/api/admin-rest/usage/rate-limits#rate-limits-header)Rate limits headerYou can check how many requests you’ve already made using the Shopify `X-Shopify-Shop-Api-Call-Limit` header that was sent in response to your API request. This header lists how many requests you’ve made for a particular store. For example:Copy91X-Shopify-Shop-Api-Call-Limit: 32/40In this example, `32` is the current request count and `40` is the bucket size.

The request count decreases according to the leak rate over time. For example, if the header displays `39/40` requests, then after a wait period of ten seconds, the header displays `19/40` requests.### [Anchor to Retry-After header](/docs/api/admin-rest/usage/rate-limits#retry-after-header)Retry-After headerWhen a request goes over a rate limit, a `429 Too Many Requests` error and a `Retry-After` header are returned. The `Retry-After` header contains the number of seconds to wait until you can make a request again. Any request made before the wait time has elapsed is throttled.Copy912X-Shopify-Shop-Api-Call-Limit: 40/40Retry-After: 2.0

## [Anchor to Resource-based rate limits](/docs/api/admin-rest/usage/rate-limits#resource-based-rate-limits)Resource-based rate limitsThe following REST Admin API resources have an additional throttle that takes effect when a store has 50,000 product variants. After this threshold is reached, no more than 1,000 new variants can be created per day.In certain cases, Shopify needs to enforce rate limiting in order to prevent abuse of the platform. Therefore, your app should be prepared to handle rate limiting on all endpoints, rather than just those listed here.PlusThese additional limits don’t apply to stores on the [Shopify Plus](https://www.shopify.com/plus) plan.**Plus:** These additional limits don’t apply to stores on the [Shopify Plus](https://www.shopify.com/plus) plan.### [Anchor to REST endpoints](/docs/api/admin-rest/usage/rate-limits#rest-endpoints)REST endpoints

-

[admin/products.json](/docs/api/admin-rest/latest/resources/product)

-

[admin/products/{product_id}.json](/docs/api/admin-rest/latest/resources/product)

-

[admin/products/{product_id}/variants.json](/docs/api/admin-rest/latest/resources/product-variant)

If an app reaches API rate limits for a specific resource, then it receives a `429 Too Many Requests` response, and a message that a throttle has been applied.

## [Anchor to Avoiding rate limit errors](/docs/api/admin-rest/usage/rate-limits#avoiding-rate-limit-errors)Avoiding rate limit errorsDesigning your app with best practices in mind is the best way to avoid throttling errors. For example, you can stagger API requests in a queue and do other processing tasks while waiting for the next queued job to run. Consider the following best practices when designing your app:

- Optimize your code to only get the data that your app requires.

- Use caching for data that your app uses often.

- Regulate the rate of your requests for smoother distribution.

- Include code that catches errors. If you ignore these errors and keep trying to make requests, then your app won’t be able to gracefully recover.

- Use metadata about your app’s API usage, included with all API responses, to manage your app’s behavior dynamically.

- Your code should stop making additional API requests until enough time has passed to retry. The recommended backoff time is 1 second.

Was this page helpful?YesNo- [Key figures](/docs/api/admin-rest/usage/rate-limits#key-figures)- [The leaky bucket algorithm](/docs/api/admin-rest/usage/rate-limits#the-leaky-bucket-algorithm)- [Rate limits](/docs/api/admin-rest/usage/rate-limits#rate-limits)- [Resource-based rate limits](/docs/api/admin-rest/usage/rate-limits#resource-based-rate-limits)- [Avoiding rate limit errors](/docs/api/admin-rest/usage/rate-limits#avoiding-rate-limit-errors)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)