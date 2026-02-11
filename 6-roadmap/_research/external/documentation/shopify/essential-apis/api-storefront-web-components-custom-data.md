---
{
  "fetch": {
    "url": "https://shopify.dev/api/storefront-web-components/custom-data",
    "fetched_at": "2026-02-10T13:39:29.966437",
    "status": 200,
    "size_bytes": 403873
  },
  "metadata": {
    "title": "Custom data",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "storefront-web-components",
    "component": "custom-data"
  }
}
---

# Custom data

# Custom dataStorefront Web Components can be used to display custom data stored in metafields and metaobjects from your Shopify store. This guide covers some of the most common ways to use custom data, and includes ready-to-use examples that you can adapt to your own storefront.Ask assistant

## [Anchor to Setup](/docs/api/storefront-web-components/custom-data#setup)SetupAlthough Storefront Web Components don't require an access token for most use cases, you need to provide a Storefront API access token to fetch metafields and metaobjects.To set up a Storefront API access token:

- Install either the [Hydrogen](https://apps.shopify.com/hydrogen) or [Headless](https://apps.shopify.com/headless) sales channel in your Shopify admin.

- Create a new storefront within the sales channel.

- Copy your public access token from your storefront settings:

**Hydrogen**: Navigate to **Storefront settings** and find the public access token in the **Storefront API** section.

- **Headless**: Inside the **Manage API access** section of your storefront, click on the **Manage** button for the Storefront API to find the public access token.

- Make sure that access is enabled for metaobjects in the **Permissions** section.

- In your Storefront Web Components code, add the public access token to the `public-access-token` attribute of your [`shopify-store` component](/docs/api/storefront-web-components/components/shopify-store).

[API docsshopify-store componentAPI docsshopify-store component](/docs/api/storefront-web-components/components/shopify-store)[API docs - shopify-store component](/docs/api/storefront-web-components/components/shopify-store)## Add a store componentCopy9123456<!-- The public-access-token is required for access to metafields and metaobjects --><shopify-store  public-access-token="your-access-token"  store-domain="your-store-domain"></shopify-store>

## [Anchor to Render a metafield](/docs/api/storefront-web-components/custom-data#render-a-metafield)Render a metafieldTo display a product's metafield data on your storefront:

- Create a [`shopify-context` component](/docs/api/storefront-web-components/components/shopify-context) that targets your specific product.

- Inside the product context, add another `shopify-context` component that targets the metafield. Specify the metafield's namespace and key as attributes. You can find the namespace and key in the [**Metafields and metaobjects**](https://www.shopify.com/admin/settings/custom_data) settings in your Shopify admin.

- Within the metafield context, use a [`shopify-data`  component](/docs/api/storefront-web-components/components/shopify-data) to display the metafield's value on the page.

Render a product metafield

This example shows how to render a product's metafield data on your storefront.Render a currency metafield

This example shows how to render a currency metafield.## Render a product metafieldCopy991234567891011121314151617181920212223242526<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><shopify-context type="product" handle="your-product-handle"> <template>   <shopify-context     type="metafield"     query="product.metafield"     key="your-metafield-key"     namespace="your-metafield-namespace"   >     <template>       <shopify-data         query="metafield.value"       ></shopify-data>     </template>   </shopify-context> </template></shopify-context>## Render a currency metafieldCopy991234567891011121314151617181920212223242526<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><shopify-context type="product" handle="your-product-handle"> <template>   <shopify-context     type="metafield"     query="product.metafield"     key="your-metafield-key"     namespace="your-metafield-namespace"   >     <template>       <shopify-money         query="metafield"       ></shopify-money>     </template>   </shopify-context> </template></shopify-context>

## [Anchor to Metafield references](/docs/api/storefront-web-components/custom-data#metafield-references)Metafield referencesYou can use a metafield to reference other objects in your store. For example, you can use a metafield on a product to reference another product. To render a metafield reference:

- Create a [`shopify-context` component](/docs/api/storefront-web-components/components/shopify-context) that targets your specific product.

- Inside the product context, add another `shopify-context` component that targets the metafield. Specify the metafield's namespace and key as attributes. You can find the namespace and key in the [**Metafields and metaobjects**](https://www.shopify.com/admin/settings/custom_data) settings in your Shopify admin.

- Within the metafield context, add another `shopify-context` component that targets the reference.

- Within the reference context, use a [`shopify-data` component](/docs/api/storefront-web-components/components/shopify-data) to display the reference's value on the page.

Render a metafield reference

This example shows how to render a metafield that references another product.Render a list of metafield references

This example shows how to render a metafield that references a list of products.Render an image from a metafield reference

This example shows how to render an image from a metafield reference.## Render a metafield referenceCopy99123456789101112131415161718192021222324252627282930313233343536373839<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><!-- A context for the product --><shopify-context type="product" handle="your-product-handle"> <template>   <!-- A context for the metafield -->   <shopify-context     type="metafield"     query="product.metafield"     key="your-metafield-key"     namespace="your-metafield-namespace"   >     <template>       <!-- A context for the product        that the metafield references -->       <shopify-context         type="product"         query="metafield.reference"       >         <template>           <div>             <shopify-data               query="product.title"             ></shopify-data>           </div>         </template>       </shopify-context>     </template>   </shopify-context> </template></shopify-context>## Render a list of metafield referencesCopy9912345678910111213141516171819202122232425262728293031323334353637383940<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><!-- A context for the product --><shopify-context type="product" handle="your-product-handle"> <template>   <!-- A context for the metafield -->   <shopify-context     type="metafield"     query="product.metafield"     key="your-metafield-key"     namespace="your-metafield-namespace"   >     <template>       <!-- A context for the product list       that the metafield references -->       <shopify-list-context         type="product"         query="metafield.references"         first="5"       >         <template>           <div>             <shopify-data               query="product.title"             ></shopify-data>           </div>         </template>       </shopify-list-context>     </template>   </shopify-context> </template></shopify-context>## Render an image from a metafield referenceCopy991234567891011121314151617181920212223242526272829303132333435363738394041<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><!-- A context for the product --><shopify-context type="product" handle="your-product-handle"> <template>   <!-- A context for the metafield -->   <shopify-context     type="metafield"     query="product.metafield"     key="your-metafield-key"     namespace="your-metafield-namespace"   >     <template>       <!-- A context for the product       that the metafield references -->       <shopify-context         type="media"         query="metafield.reference"       >         <template>           <div>             <shopify-media               query="media"               width="100"               height="100"             ></shopify-media>           </div>         </template>       </shopify-context>     </template>   </shopify-context> </template></shopify-context>

## [Anchor to Render a metaobject](/docs/api/storefront-web-components/custom-data#render-a-metaobject)Render a metaobjectMetaobjects are dynamic objects that store custom data in your Shopify store. You can render metaobjects using Storefront Web Components with a [shopify-context component](/docs/api/storefront-web-components/components/shopify-context):

- Create a `shopify-context` component with `type="metaobject"` and `handle` attributes. The `handle` attribute specifies which metaobject to render. You can find the handle values for each metaobject on the [**Entries**](https://www.shopify.com/admin/content/metaobjects/entries) page in your Shopify admin.

- Add a `metaobject-definition-type` attribute to the same `shopify-context` component to specify the metaobject definition type.

- To access metafields within the metaobject, add a nested [`shopify-context` component](/docs/api/storefront-web-components/components/shopify-context) with `type="field"` and `key` attributes. The `key` attribute identifies which metafield to target. You can find the key values for each metafield in the [**Metafields and metaobjects**](https://www.shopify.com/admin/settings/custom_data) settings in your Shopify admin.

- Inside the metafield context, add your template and components to display the metafield data.

Render a metaobject

This example shows how to render metafields within a metaobject.Render a list of metaobjects

This example shows how to render a list of metaobjects with a [shopify-list-context component](/docs/api/storefront-web-components/components/shopify-list-context).Render a metaobject reference

This example shows how to render a product and image reference from a metaobject.## Render a metaobjectCopy991234567891011121314151617181920212223242526272829303132<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><!-- A context for the metaobject. It must contain a metaobject attribute with the metaobject name --><shopify-context type="metaobject" handle="your-metaobject-handle" metaobject-definition-type="your-metaobject-definition-type"> <template>   <!-- A context for the metafield.    It must contain the metafield key -->   <shopify-context     type="field"     query="metaobject.field"     key="your-metafield-key"   >     <template>       <div>         <shopify-data           query="field.value"         ></shopify-data>       </div>     </template>   </shopify-context> </template></shopify-context>## Render a list of metaobjectsCopy9912345678910111213141516171819202122232425262728293031323334<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><!-- A context for the metaobject. It must containa metaobject attribute with the metaobject name --><shopify-list-context type="metaobject" query="metaobjects" metaobject-definition-type="stores" first="10"> <!-- The template is repeated for each metaobject in the list --> <template>    <!-- A context for the metafield.    It must contain the metafield key -->   <shopify-context     type="field"     query="metaobject.field"     key="title"   >     <template>       <div>         <shopify-data           query="field.value"         ></shopify-data>       </div>     </template>   </shopify-context> </template></shopify-list-context>## Render a metaobject referenceCopy991234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556<!-- The public-access-token is required for access to metafields and metaobjects --> <shopify-store public-access-token="your-access-token" store-domain="your-store-domain"></shopify-store><!-- A context for the metaobject. It must contain a metaobject attribute with the metaobject name --><shopify-context type="metaobject" handle="your-metaobject-handle" metaobject-definition-type="your-metaobject-definition-type"> <template>   <!-- A context for the product metafield.    It must contain the metafield key -->   <shopify-context     type="field"     query="metaobject.field"     key="your-product-metafield-key"   >     <template>      <!-- A context for the product reference -->      <shopify-context type="product" query="field.reference">        <template>          <div>            <shopify-data query="product.title"></shopify-data>          </div>        </template>      </shopify-context>     </template>   </shopify-context>   <!-- A context for the image metafield.    It must contain the metafield key -->   <shopify-context     type="field"     query="metaobject.field"     key="your-image-metafield-key"   >     <template>      <!-- A context for the image reference.       The type must match the Storefront API       object type of the metafield reference -->      <shopify-context type="media" query="field.reference">        <template>          <div>            <shopify-media query="media"></shopify-media>          </div>        </template>      </shopify-context>     </template>   </shopify-context> </template></shopify-context>

## [Anchor to Custom components](/docs/api/storefront-web-components/custom-data#custom-components)Custom componentsMetafields support various data types, including rich text, links, numbers, dates, JSON, and file references. The [`shopify-data` component](/docs/api/storefront-web-components/components/shopify-data) displays the raw metafield value as-is. For more sophisticated presentations of complex data types like JSON objects or structured content, you can build custom components that receive the metafield value as an attribute with the [`shopify-attr` attribute](/docs/api/storefront-web-components/attributes/shopify-attr).[API docsshopify-attr attributeAPI docsshopify-attr attribute](/docs/api/storefront-web-components/attributes/shopify-attr)[API docs - shopify-attr attribute](/docs/api/storefront-web-components/attributes/shopify-attr)## Add a custom componentCopy99123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354<script>  // Define a custom component that renders a JSON object  class CustomComponent extends HTMLElement {    constructor() {      super();    }    connectedCallback() {      const value = JSON.parse(        this.getAttribute("value"),      );      this.innerHTML = `        <div>          <h1>${value.title}</h1>          <p>${value.description}</p>        </div>      `;    }  }  // Register the custom component  customElements.define(    "custom-component",    CustomComponent,  );</script><!-- The public-access-token is required  for access to metafields and metaobjects --><shopify-store  public-access-token="your-access-token"  store-domain="your-store-domain"></shopify-store><shopify-context  type="product"  handle="your-product-handle">  <template>    <shopify-context      type="metafield"      query="product.metafield"      key="your-metafield-key"      namespace="your-metafield-namespace"    >      <template>        <!-- Bind the metafield value to the        value attribute of the custom component -->        <custom-component          shopify-attr--value="metafield.value"        ></custom-component>      </template>    </shopify-context>  </template></shopify-context>

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)