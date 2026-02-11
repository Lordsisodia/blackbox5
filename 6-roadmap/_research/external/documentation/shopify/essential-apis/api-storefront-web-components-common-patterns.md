---
{
  "fetch": {
    "url": "https://shopify.dev/api/storefront-web-components/common-patterns",
    "fetched_at": "2026-02-10T13:39:28.120428",
    "status": 200,
    "size_bytes": 333204
  },
  "metadata": {
    "title": "Common patterns",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "storefront-web-components",
    "component": "common-patterns"
  }
}
---

# Common patterns

# Common patternsStorefront Web Components can be customized for many different applications. This guide covers some of the most common ways they can be used to sell online, and includes ready-to-use examples that you can adapt to your own storefront. To learn more, see the [component documentation](/docs/api/storefront-web-components/components/shopify-cart).Ask assistant

## [Anchor to Buy now button](/docs/api/storefront-web-components/common-patterns#buy-now-button)Buy now buttonAdd a button that redirects the customer to a Shopify-hosted checkout page. This is useful when you want to sell a single product.To create a "Buy now" button:

-

Add a `button` component inside a [shopify-context component](/docs/api/storefront-web-components/components/shopify-context) that's associated with a product.

-

Call the `buyNow()` method in the `button` component's `onclick` attribute.

The method needs an event object where the event target must be inside a product [context component](/docs/api/storefront-web-components/components/shopify-context).

- The component will redirect the customer to the checkout page with the selected product.

-

Customize the state and location of the checkout page:

Add discount codes by passing them in the options parameter: `{discountCodes: ['CODE1', 'CODE2']}`

- Set the target window or tab for the checkout page: `{target: '_blank'}`

- Combine both: `{discountCodes: ['SAVE10'], target: '_blank'}`

-

Configure the button state with the `shopify-attr--disabled` attribute. You can use this to automatically disable the button when the product variant is not available for sale.

NoteYou can mix "Buy now" buttons from different stores on the same page. Each button will open the checkout page of its own store.**Note:** You can mix "Buy now" buttons from different stores on the same page. Each button will open the checkout page of its own store.'Buy now' button example

Add a button that redirects the customer to a Shopify-hosted checkout page.Include discount codes

Add discount codes to the checkout. This applies the discount codes automatically when the customer reaches checkout.Sell from multiple stores

Use "Buy now" buttons from multiple stores on the same page. Each button will open the checkout page of its own store.Set a custom target window

Choose where the checkout page opens by setting the target as a new tab or the same tab. You can also specify discount codes that will be applied to the cart.## Buy now button exampleCopy9912345678910111213141516171819202122232425<shopify-store  id="store"  store-domain="https://your-store.myshopify.com"></shopify-store><!-- The context is bound to the store --><shopify-context  type="product"  handle="handle-of-product"><template>  <shopify-variant-selector></shopify-variant-selector>  <!-- The product added will be whatever  variant is selected for the context product handle.  The disabled attribute is added if the variant is not available for sale.  -->  <button    onclick="getElementById('store').buyNow(event);"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Buy now  </button></template></shopify-context>## Use discount codes with 'Buy now' buttonsCopy9912345678910111213141516171819202122232425262728<shopify-store  store-domain="https://your-store.myshopify.com"></shopify-store><shopify-context  type="product"  handle="handle-of-product"><template>  <shopify-variant-selector></shopify-variant-selector>  <!-- Checkout opens with discount codes applied automatically -->  <button    onclick="buyNowWithDiscount(event)"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Buy now with discount  </button>    <script>    function buyNowWithDiscount(event) {      document.querySelector('shopify-store').buyNow(event, {        discountCodes: ['SAVE10', 'FREESHIP']      });    }  </script></template></shopify-context>## Sell from multiple storesCopy9912345678910111213141516171819202122232425262728293031323334353637383940414243<!-- First store --><shopify-store  store-domain="https://your-first-store.myshopify.com">  <shopify-context    type="product"    handle="snowboard"  >  <template>    <h2>Product from Store 1</h2>    <h3><shopify-data query="product.title"></shopify-data></h3>    <shopify-variant-selector></shopify-variant-selector>    <button      onclick="document.querySelector('shopify-store').buyNow(event);"      shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"    >      Buy now from Store 1    </button>  </template>  </shopify-context></shopify-store><!-- Second store --><shopify-store  store-domain="https://your-second-store.myshopify.com">  <shopify-context    type="product"    handle="t-shirt"  >  <template>    <h2>Product from Store 2</h2>    <h3><shopify-data query="product.title"></shopify-data></h3>    <shopify-variant-selector></shopify-variant-selector>    <button      onclick="document.querySelector('shopify-store').buyNow(event);"      shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"    >      Buy now from Store 2    </button>  </template>  </shopify-context></shopify-store>## Custom target windowCopy9912345678910111213141516171819202122232425262728293031323334353637<shopify-store  store-domain="https://your-store.myshopify.com"></shopify-store><shopify-context  type="product"  handle="handle-of-product"><template>  <shopify-variant-selector></shopify-variant-selector>    <!-- Buy now opening in the same tab -->  <button    onclick="document.querySelector('shopify-store').buyNow(event, {target: '_self'});"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Buy now (same tab)  </button>    <!-- Buy now opening in a new tab -->  <button    onclick="document.querySelector('shopify-store').buyNow(event, {target: '_blank'});"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Buy now (new tab)  </button>    <!-- Buy now with discount codes and custom target -->  <button    onclick="document.querySelector('shopify-store').buyNow(event, {target: '_blank', discountCodes: ['SAVE10']});"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Buy now with discount (new tab)  </button></template></shopify-context>

## [Anchor to Add to cart button](/docs/api/storefront-web-components/common-patterns#add-to-cart-button)Add to cart buttonAdd a button that lets customers add your products to their cart. This is useful when you want to sell multiple products, because it lets customers add products to their cart without being redirected from your site to the checkout page.To create an "Add to cart" button:

-

Add a `button` component inside a [shopify-context component](/docs/api/storefront-web-components/components/shopify-context) that's associated with a product.

-

Call the `addLine()` method in the `button` component's `onclick` attribute to add the product to the customer's cart.

This method requires an event object or a product data object.

- If using an event, the event target must be inside a product [context component](/docs/api/storefront-web-components/components/shopify-context).

-

Display the cart using a native [HTML `<dialog>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog).

To show it as a popup modal, call the `showModal()` method.

-

Customize the cart's styling and content with CSS parts and slots. [View examples](/docs/api/storefront-web-components/components/shopify-cart#examples)

NoteThe cart component doesn't support mixing products from multiple stores.**Note:** The cart component doesn't support mixing products from multiple stores.[API docsshopify-cart componentAPI docsshopify-cart component](/docs/api/storefront-web-components/components/shopify-cart)[API docs - shopify-cart component](/docs/api/storefront-web-components/components/shopify-cart)## Add to cart exampleCopy991234567891011121314151617181920212223242526<shopify-store  store-domain="https://your-store.myshopify.com"></shopify-store><!-- The context is bound to the store --><shopify-context  type="product"  handle="handle-of-product"><template>  <shopify-variant-selector></shopify-variant-selector>  <!-- The product added will be whatever  variant is selected for the context product handle.  The disabled attribute is added if the variant is not available for sale.  -->  <button    onclick="getElementById('cart').addLine(event).showModal();"    shopify-attr--disabled="!product.selectedOrFirstAvailableVariant.availableForSale"  >    Add to cart  </button></template></shopify-context><shopify-cart id="cart"></shopify-cart>

## [Anchor to Product details dialog](/docs/api/storefront-web-components/common-patterns#product-details-dialog)Product details dialogAdd a button that lets customers view details about a product on a separate dialog. This is useful if you have limited space on your page, but still want to provide a way for customers to view product details.To create a "View details" button":

-

Add an HTML `<dialog>` element to your page. Inside the dialog, place a product [shopify-context component](/docs/api/storefront-web-components/components/shopify-context) with a `wait-for-update` attribute. The `wait-for-update` attribute prevents the dialog from loading product details until a specific product is selected. Include a template and components within the product context to display the product information.

-

Add a `button` element inside another [shopify-context component](/docs/api/storefront-web-components/components/shopify-context) that's associated with a product.

-

Add a click event listener to the button that calls the [update method](/docs/api/storefront-web-components/components/shopify-context#attributes-propertydetail-update) on the product context inside the dialog. This links the dialog's product context (destination) with the product context nearest to the button (source), allowing the dialog to display details for the selected product.

-

Display the dialog by calling the native [`showModal`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal) method.

## Product details exampleCopy991234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859<shopify-store  store-domain="https://your-store.myshopify.com"  country="CA"  language="FR"></shopify-store><script>  function showProductDetails(event) {    // Update a dialog context with a selected product    document.getElementById('dialog-context')      .update(event);    // Show the dialog    document.getElementById('dialog')      .showModal();  }</script><!-- A list of products --><shopify-list-context  type="product"  query="products"  first="10">  <!-- This template is repeated for each product-->  <template>    <!-- A button that shows the product details -->    <button      onclick="showProductDetails(event)"    >      <shopify-data        query="product.title"      ></shopify-data>    </button>  </template></shopify-list-context><dialog id="dialog">  <!-- A product context that waits for an update to render -->  <shopify-context    id="dialog-context"    type="product"    wait-for-update  >    <template>      <div>        <shopify-data          query="product.description"        ></shopify-data>      </div>    </template>    <div      shopify-loading-placeholder    >      Loading...    </div>  </shopify-context></dialog>

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)