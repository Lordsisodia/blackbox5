---
{
  "fetch": {
    "url": "https://shopify.dev/api/storefront-web-components/getting-started",
    "fetched_at": "2026-02-10T13:39:26.474229",
    "status": 200,
    "size_bytes": 301173
  },
  "metadata": {
    "title": "Getting started",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "storefront-web-components",
    "component": "getting-started"
  }
}
---

# Getting started

# Getting startedThis guide provides step-by-step instructions for adding Storefront Web Components to your website. If you want to use an LLM to generate code, include the [LLMs.txt](https://webcomponents.shopify.dev/llms.txt) file with your prompt to guide the model's output.Ask assistant

## [Anchor to Step 1: Connect your store](/docs/api/storefront-web-components/getting-started#step-1-connect-your-store)Step 1: Connect your storeOpen the HTML file in the project where you want to use Storefront Web Components, and add the script tag shown here. Beneath it, add a [`<shopify-store>` component](/docs/api/storefront-web-components/components/shopify-store), with the domain of your store (for example, `https://demostore.mock.shop/`).The `<shopify-store>` component supports optional country and language attributes that let you display pricing and content for a specific market.You don't need an access token to use Storefront Web Components. However, if you want to display the inventory count or any custom data about a product, then you need to add an access token to the `<shopify-store>` component as well. To get an access token:

- Install the [Headless channel](https://apps.shopify.com/headless) from the Shopify App Store.

- To generate an access token, navigate to the Headless channel in your Shopify admin and click **Create storefront**.

- In the **Manage API access** section, click **Manage** for the Storefront API, and then copy the public access token.

- In your project, add a `public-access-token` attribute with your token to the `<shopify-store>` component (for example, `public-access-token="your-access-token"`).

Using LLMs with Storefront Web ComponentsIf you want to use an LLM to generate code, include the [LLMs.txt](https://webcomponents.shopify.dev/llms.txt) file with your prompt to guide the model's output.**Using LLMs with Storefront Web Components:** If you want to use an LLM to generate code, include the [LLMs.txt](https://webcomponents.shopify.dev/llms.txt) file with your prompt to guide the model's output.## Storefront Web Components setupCopy9123456789<script src="https://cdn.shopify.com/storefront/web-components.js"></script><shopify-store  store-domain="https://your-store.myshopify.com"  country="US"  language="en"></shopify-store>

## [Anchor to Step 2: Set the context](/docs/api/storefront-web-components/getting-started#step-2-set-the-context)Step 2: Set the contextAfter adding the script tag and `<shopify-store>` component, add a [`<shopify-context>` component](/docs/api/storefront-web-components/components/shopify-context). This defines which Shopify data will be available.Each `<shopify-context>` component requires two attributes:

- `type`: Specifies what kind of data you want (for example, `product`).

- `handle`: Identifies the specific item. For example, the handle for the URL [`demostore.mock.shop/products/men-t-shirt`](https://demostore.mock.shop/products/men-t-shirt) is `men-t-shirt`.

If you're working with a single storefront, then you can add the `<shopify-context>` component anywhere on your page (it doesn't need to be inside the `<shopify-store>` component). If you're working with multiple storefronts, then nest the context inside its corresponding store component.Every `<shopify-context>` component also requires a template component, which contains the data you want to display. That template won't render until the context loads. You'll populate this component in the next step.## Setup contextCopy9912345678910111213141516<script src="https://cdn.shopify.com/storefront/web-components.js"></script><shopify-store  store-domain="https://your-store.myshopify.com"></shopify-store><shopify-context  type="product"  handle="your-product-handle">  <template>    <!-- This template won't be rendered until the context is loaded -->  </template></shopify-context>

## [Anchor to Step 3: Load Shopify data](/docs/api/storefront-web-components/getting-started#step-3-load-shopify-data)Step 3: Load Shopify dataInside a context template, you can use any standard HTML markup along with Shopify's data components.The [`shopify-data`](/docs/api/storefront-web-components/components/shopify-data) component is used to display Shopify data on your page. Here's how it works:

- It requires a `query` attribute that specifies which data to display.

- The query uses dot notation to access data fields (for example, `query="product.title"`).

- It looks for the nearest matching `<shopify-context>` component to find the data.

- It outputs plain text that you can style with your own HTML elements.

In this example, `<shopify-data query="product.title">` finds the nearest product context (based on its `handle` attribute), accesses its `title` property, and displays it as text.Since the component outputs a text node, to match your site's design you can wrap it in any necessary HTML elements. The component also supports rich text fields like `product.descriptionHtml`.## Data loadingCopy9912345678910111213141516171819202122232425<script src="https://cdn.shopify.com/storefront/web-components.js"></script><shopify-store  store-domain="https://your-store.myshopify.com"></shopify-store><shopify-context  type="product"  handle="your-product-handle">  <template>    <!-- shopify-data renders a text node -->    <h1 class="your-style">      <shopify-data query="product.title">      </shopify-data>    </h1>    <p>      <!-- This renders a rich text description -->      <shopify-data query="product.descriptionHtml">      </shopify-data>    </p>  </template></shopify-context>

## [Anchor to Step 4: Format components](/docs/api/storefront-web-components/getting-started#step-4-format-components)Step 4: Format componentsSome types of data , like `currency` and `media`, require extra formatting to display properly. For these types of data, you can use the following components:

- [`shopify-money`](/docs/api/storefront-web-components/components/shopify-money): Accepts a query reference to a money object, and uses the store's country and language market to format it correctly.

- [`shopify-media`](/docs/api/storefront-web-components/components/shopify-media): Accepts an image reference and generates an image element with `srcset` and `sizes` attributes.

## Formatting componentsCopy9912345678910111213141516171819202122232425262728<script src="https://cdn.shopify.com/storefront/web-components.js"></script><shopify-store  store-domain="https://your-store.myshopify.com"></shopify-store><shopify-context  type="product"  handle="your-product-handle">  <template>    <!-- Display the product price -->    <shopify-money      query="product.selectedOrFirstAvailableVariant.price"      format="money_with_currency">    </shopify-money>    <!-- Display the product image -->    <shopify-media      query="product.selectedOrFirstAvailableVariant.image"      width="400"      height="400"    >    </shopify-media>  </template></shopify-context>

## [Anchor to Step 5: Connect to checkout](/docs/api/storefront-web-components/getting-started#step-5-connect-to-checkout)Step 5: Connect to checkoutYou can add buttons to your components that let customers buy products, view product details, or [add products to their cart](/docs/api/storefront-web-components/components/shopify-cart).To add a "Buy now" button that redirects the customer to the checkout page:

-

Add a `button` component inside a [shopify-context component](/docs/api/storefront-web-components/components/shopify-context) that's associated with a product.

-

Call the `buyNow()` method in the `button` component's `onclick` attribute, and make sure it includes an event object whose target is inside a `shopify-context` component.

When the customer clicks the button, the component will redirect them to the checkout page with the selected product.To learn more about different button actions, see [Common patterns](/docs/api/storefront-web-components/common-patterns).## Buy now button exampleCopy9912345678910111213141516171819202122232425<shopify-store  id="store"  store-domain="https://your-store.myshopify.com"></shopify-store><!-- The context is bound to the store --><shopify-context  type="product"  handle="handle-of-product"><template>  <shopify-variant-selector></shopify-variant-selector>  <!-- The product added will be whatever  variant is selected for the context product handle.  The disabled attribute is added if the variant is not available for sale.  -->  <button    onclick="getElementById('store').buyNow(event);"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Buy now  </button></template></shopify-context>

## [Anchor to Next steps](/docs/api/storefront-web-components/getting-started#next-steps)Next stepsNow that you've set up the basic Storefront Web Components, you can use others to add new types of data or functionality to your website. Components are available for common commerce features and design patterns, including:

- [`shopify-list-context`](/docs/api/storefront-web-components/components/shopify-list-context): Displays multiple items in a repeating format, like a list of products or collections.

- [`shopify-cart`](/docs/api/storefront-web-components/components/shopify-cart): Provides simple shopping cart using a native [HTML `<dialog>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog).

- [`shopify-variant-selector`](/docs/api/storefront-web-components/components/shopify-variant-selector): Creates a form that lets customers choose between different product options (like sizes, colors, or materials).

[ExploreStorefront Web Components playgroundExploreStorefront Web Components playground](https://webcomponents.shopify.dev/playground)[Explore - Storefront Web Components playground](https://webcomponents.shopify.dev/playground)[Learn moreStorefront Web Components referenceLearn moreStorefront Web Components reference](/docs/api/storefront-web-components/components/shopify-cart)[Learn more - Storefront Web Components reference](/docs/api/storefront-web-components/components/shopify-cart)

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)