---
{
  "fetch": {
    "url": "https://shopify.dev/docs/api/admin-extensions/2026-01/polaris-web-components/forms/dropzone",
    "fetched_at": "2026-02-10T13:29:49.735445",
    "status": 200,
    "size_bytes": 286552
  },
  "metadata": {
    "title": "DropZone",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "forms",
    "component": "dropzone"
  }
}
---

# DropZone

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest# DropZoneAsk assistantLets users upload files through drag-and-drop functionality into a designated area on a page, or by activating a button.

## [Anchor to properties](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties)Properties[Anchor to accept](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-accept)accept**accept**string**string**Default: ''**Default: ''**A string representing the types of files that are accepted by the drop zone. This string is a comma-separated list of unique file type specifiers which can be one of the following:

- A file extension starting with a period (".") character (e.g. .jpg, .pdf, .doc)

- A valid MIME type string with no extensions

If omitted, all file types are accepted.

[Anchor to accessibilityLabel](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-accessibilitylabel)accessibilityLabel**accessibilityLabel**string**string**A label that describes the purpose or contents of the item. When set, it will be announced to buyers using assistive technologies and will provide them with more context.

[Anchor to disabled](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-disabled)disabled**disabled**boolean**boolean**Default: false**Default: false**Disables the field, disallowing any interaction.

[Anchor to error](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-error)error**error**string**string**Indicate an error to the user. The field will be given a specific stylistic treatment to communicate problems that have to be resolved immediately.

[Anchor to files](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-files)files**files**File[]**File[]**Default: []**Default: []**An array of File objects representing the files currently selected by the user.

This property is read-only and cannot be directly modified. To clear the selected files, set the `value` prop to an empty string or null.

[Anchor to label](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-label)label**label**string**string**Content to use as the field label.

[Anchor to labelAccessibilityVisibility](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-labelaccessibilityvisibility)labelAccessibilityVisibility**labelAccessibilityVisibility**"visible" | "exclusive"**"visible" | "exclusive"**Default: 'visible'**Default: 'visible'**Changes the visibility of the component's label.

- `visible`: the label is visible to all users.

- `exclusive`: the label is visually hidden but remains in the accessibility tree.

[Anchor to multiple](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-multiple)multiple**multiple**boolean**boolean**Default: false**Default: false**Whether multiple files can be selected or dropped at once.

[Anchor to name](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-name)name**name**string**string**An identifier for the field that is unique within the nearest containing form.

[Anchor to required](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-required)required**required**boolean**boolean**Default: false**Default: false**Whether the field needs a value. This requirement adds semantic value to the field, but it will not cause an error to appear automatically. If you want to present an error when this field is empty, you can do so with the `error` property.

[Anchor to value](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#properties-propertydetail-value)value**value**string**string**Default: ''**Default: ''**This sets the input value for a file type, which cannot be set programatically, so it can only be reset.

## [Anchor to events](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#events)EventsLearn more about [registering events](/docs/api/app-home/using-polaris-components#event-handling).

[Anchor to change](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#events-propertydetail-change)change**change**CallbackEventListenerCallbackEventListener<typeof tagName$K>**CallbackEventListenerCallbackEventListener<typeof tagName$K>**[Anchor to droprejected](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#events-propertydetail-droprejected)droprejected**droprejected**CallbackEventListenerCallbackEventListener<typeof tagName$K>**CallbackEventListenerCallbackEventListener<typeof tagName$K>**[Anchor to input](/docs/api/admin-extensions/latest/polaris-web-components/forms/dropzone#events-propertydetail-input)input**input**CallbackEventListenerCallbackEventListener<typeof tagName$K>**CallbackEventListenerCallbackEventListener<typeof tagName$K>**### CallbackEventListener```

(EventListener & {

(event: CallbackEvent<T>): void;

}) | null

```### CallbackEvent```

Event & {

currentTarget: HTMLElementTagNameMap[T];

}

```ExamplesCodejsxhtmlCopy9123456789<s-drop-zone  label="Upload"  accessibilityLabel="Upload image of type jpg, png, or gif"  accept=".jpg,.png,.gif"  multiple  onInput={(event) => console.log('onInput', event.currentTarget?.value)}  onChange={(event) => console.log('onChange', event.currentTarget?.value)}  onDropRejected={(event) => console.log('onDropRejected', event.currentTarget?.value)} />## Preview### Examples- #### Codejsx```

<s-drop-zone

label="Upload"

accessibilityLabel="Upload image of type jpg, png, or gif"

accept=".jpg,.png,.gif"

multiple

onInput={(event) => console.log('onInput', event.currentTarget?.value)}

onChange={(event) => console.log('onChange', event.currentTarget?.value)}

onDropRejected={(event) => console.log('onDropRejected', event.currentTarget?.value)}

/>

```html```

<s-drop-zone

label="Upload"

accessibilityLabel="Upload image of type jpg, png, or gif"

accept=".jpg,.png,.gif"

multiple

onInput="console.log('onInput', event.currentTarget?.value)"

onChange="console.log('onChange', event.currentTarget?.value)"

onDropRejected="console.log('onDropRejected', event.currentTarget?.value)"

></s-drop-zone>

```- #### Basic usageDescriptionDemonstrates a basic drop zone that allows multiple file uploads with a simple label.jsx```

<s-drop-zone label="Drop files to upload" multiple />

```html```

<s-drop-zone label="Drop files to upload" multiple></s-drop-zone>

```- #### Image uploadDescriptionShows a drop zone configured specifically for uploading multiple image files.jsx```

<s-drop-zone accept="image/*" label="Upload images" multiple />

```html```

<s-drop-zone accept="image/*" label="Upload images" multiple></s-drop-zone>

```- #### With required fieldDescriptionIllustrates a drop zone when the file upload is required.jsx```

<s-drop-zone name="file" required label="Upload file" />

```html```

<s-drop-zone name="file" required label="Upload file"></s-drop-zone>

```- #### Disabled stateDescriptionDisplays a drop zone in a disabled state, preventing file uploads.jsx```

<s-drop-zone label="Upload not available" disabled />

```html```

<s-drop-zone label="Upload not available" disabled></s-drop-zone>

```- #### File type restrictionsDescriptionDemonstrates restricting file uploads to specific document types like PDF and DOC.jsx```

<s-drop-zone

accept=".pdf,.doc,.docx"

label="Upload documents"

multiple

/>

```html```

<s-drop-zone

accept=".pdf,.doc,.docx"

label="Upload documents"

multiple

></s-drop-zone>

```- #### With error stateDescriptionShows a drop zone with an error message, useful for indicating file upload validation issues.jsx```

<s-drop-zone

label="Upload file"

error="File size must be less than 5mb"

/>

```html```

<s-drop-zone

label="Upload file"

error="File size must be less than 5mb"

></s-drop-zone>

```- #### With accessibility optionsDescriptionIllustrates advanced accessibility configuration for the drop zone, including custom accessibility labels.jsx```

<s-drop-zone

label="Upload files"

accessibilityLabel="Upload files using drag and drop or file selector"

labelAccessibilityVisibility="exclusive"

multiple

/>

```html```

<s-drop-zone

label="Upload files"

accessibilityLabel="Upload files using drag and drop or file selector"

labelAccessibilityVisibility="exclusive"

multiple

></s-drop-zone>

```Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)