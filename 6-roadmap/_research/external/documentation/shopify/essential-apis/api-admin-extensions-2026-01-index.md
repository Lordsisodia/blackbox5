---
{
  "fetch": {
    "url": "https://shopify.dev/api/admin-extensions/2026-01/index",
    "fetched_at": "2026-02-10T13:40:09.207847",
    "status": 200,
    "size_bytes": 418060
  },
  "metadata": {
    "title": "Admin UI extensions",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "2026-01",
    "component": "index"
  }
}
---

# Admin UI extensions

# Admin UI extensionsAdmin UI extensions make it possible to surface contextual app functionality within the Shopify Admin interface.Ask assistant

Choose a version:2026-01 latest2025-10 2025-07 2025-04 2025-01 2024-10 2024-07 2024-04 2024-01 2023-10 2026-01latest

## [Anchor to Getting started](/docs/api/admin-extensions/latest/index#getting-started)Getting startedUse the [Shopify CLI](/docs/api/shopify-cli) to [generate a new extension](/apps/tools/cli/commands#generate-extension) within your app.If you already have a Shopify app, you can skip right to the last command shown here.Make sure you're using Shopify CLI `v3.85.3` or higher. You can check your version by running `shopify version`.## Generate an extensionCopy## CLI9912345678910# create an app if you don't already have one:shopify app init --name my-app# navigate to your app's root directory:cd my-app# generate a new extension:shopify app generate extension# follow the steps to create a new# extension in ./extensions.

## [Anchor to Optional ESLint configuration](/docs/api/admin-extensions/latest/index#optional-eslint-configuration)Optional ESLint configurationIf your app is using ESLint, update your configuration to include the new global `shopify` object.## .eslintrc.cjsCopy912345module.exports = {  globals: {    shopify: 'readonly',  },};

## [Anchor to Scaffolded with Preact](/docs/api/admin-extensions/latest/index#scaffolded-with-preact)Scaffolded with PreactUI Extensions are scaffolded with [Preact](https://preactjs.com/) by default.This means that you can use Preact patterns and principles within your extension. Since Preact is included as a standard dependency, you have access to all of its features including [hooks](https://preactjs.com/guide/v10/hooks/) like `useState` and `useEffect` for managing component state and side effects.You can also use [Preact Signals](https://preactjs.com/guide/v10/signals) for reactive state management, and take advantage of standard web APIs just like you would in a regular Preact application.## Scaffolded with PreactCopy## JSX991234567891011121314151617181920import '@shopify/ui-extensions/preact';import {render} from 'preact';import {useState} from 'preact/hooks';export default async () => {  render(<Extension />, document.body);}function Extension() {  const [count, setCount] = useState(0);  return (    <>      <s-text>Count: {count}</s-text>      <s-button onClick={() => setCount(count + 1)}>        Increment      </s-button>    </>  );}

## [Anchor to Handling events](/docs/api/admin-extensions/latest/index#handling-events)Handling eventsHandling events in UI extensions are the same as you would handle them in a web app. You can use the `addEventListener` method to listen for events on the components or use the `on[event]` property to listen for events from the components.When using Preact, event handlers can be registered by passing props beginning with `on`, and the event handler name is case-insensitive. For example, the JSX `<s-button onClick={fn}>` registers `fn` as a "click" event listener on the button.## Handling eventsCopy## JSX9912345678910111213141516171819export default function HandlingEvents() {  const handleClick = () => {    console.log('s-button clicked');  };  return <s-button onClick={handleClick}>Click me</s-button>;}// orexport default function HandlingEvents() {  const handleClick = () => {    console.log('s-button clicked');  };  const button = document.createElement('s-button');  button.addEventListener('click', handleClick);  document.body.appendChild(button);}

## [Anchor to Using forms](/docs/api/admin-extensions/latest/index#using-forms)Using formsWhen building a Block extension you may use the [Form component](/docs/api/admin-extensions/latest/components/forms/form) to integrate with the contextual save bar of the resource page. The Form component provides a way to manage form state and submit data to your app's backend or directly to Shopify using Direct API access.Whenever an input field is changed, the Form component will automatically update the dirty state of the resource page. When the form is submitted or reset the relevant callback in the form component will get triggered.Using this, you can control what defines a component to be dirty by utilizing the Input's defaultValue property.Rules:

-

When the defaultValue is set, the component will be considered dirty if the value of the input is different from the defaultValue.You may update the defaultValue when the form is submitted to reset the dirty state of the form.

-

When the defaultValue is not set, the component will be considered dirty if the value of the input is different from the initial value or from the last dynamic update to the input's value that wasn't triggered by user input.

Note: In order to trigger the dirty state, each input must have a name attribute.

## Trigger the Form's dirty stateUsing `defaultValue`Using implicit defaultCopy99123456789101112131415161718192021222324252627282930313233343536const defaultValues = {  text: 'default value',  number: 50,};const [textValue, setTextValue] = useState('');const [numberValue, setNumberValue] = useState('');return (  <s-admin-block title="My Block Extension">    <s-form      onSubmit={(event) => {        event.waitUntil(fetch('app:save/data'));        console.log('submit', {textValue, numberValue});      }}      onReset={() => console.log('automatically reset values')}    >      <s-stack direction="block" gap="base">        <s-text-field          label="Default Value"          name="my-text"          defaultValue={defaultValues.text}          value={textValue}          onChange={(e) => setTextValue(e.currentTarget.value)}        />        <s-number-field          label="Percentage field"          name="my-number"          defaultValue={defaultValues.number}          value={numberValue}          onChange={(e) => setNumberValue(e.currentTarget.value)}        />      </s-stack>    </s-form>  </s-admin-block>);99123456789101112131415161718192021222324252627282930313233343536373839404142434445import { render } from 'preact';import { useState } from 'preact/hooks';export default async () => {  render(<Extension />, document.body);}async function Extension() {  const data = await fetch('/data.json');  const {text, number} = await data.json();  return <App text={text} number={number} />;}function App({text, number}) {  // The initial values set in the form fields will be the default values  const [textValue, setTextValue] = useState(text);  const [numberValue, setNumberValue] = useState(number);  return (    <s-admin-block title="My Block Extension">      <s-form        onSubmit={(event) => {          event.waitUntil(fetch('app:data/save'));          console.log('submit', {textValue, numberValue});        }        onReset={() => console.log('automatically reset values')}      >        <s-stack direction="block" gap="base">          <s-text-field            label="Default Value"            name="my-text"            value={textValue}            onChange={(e) => setTextValue(e.currentTarget.value)}          />          <s-number-field            label="Percentage field"            name="my-number"            value={numberValue}            onChange={(e) => setNumberValue(e.currentTarget.value)}          />        </s-stack>      </s-form>    </s-admin-block>  );}Using `defaultValue````

const defaultValues = {

text: 'default value',

number: 50,

};

const [textValue, setTextValue] = useState('');

const [numberValue, setNumberValue] = useState('');

return (

<s-admin-block title="My Block Extension">

<s-form

onSubmit={(event) => {

event.waitUntil(fetch('app:save/data'));

console.log('submit', {textValue, numberValue});

}}

onReset={() => console.log('automatically reset values')}

>

<s-stack direction="block" gap="base">

<s-text-field

label="Default Value"

name="my-text"

defaultValue={defaultValues.text}

value={textValue}

onChange={(e) => setTextValue(e.currentTarget.value)}

/>

<s-number-field

label="Percentage field"

name="my-number"

defaultValue={defaultValues.number}

value={numberValue}

onChange={(e) => setNumberValue(e.currentTarget.value)}

/>

</s-stack>

</s-form>

</s-admin-block>

);

```Using implicit default```

import { render } from 'preact';

import { useState } from 'preact/hooks';

export default async () => {

render(<Extension />, document.body);

}

async function Extension() {

const data = await fetch('/data.json');

const {text, number} = await data.json();

return <App text={text} number={number} />;

}

function App({text, number}) {

// The initial values set in the form fields will be the default values

const [textValue, setTextValue] = useState(text);

const [numberValue, setNumberValue] = useState(number);

return (

<s-admin-block title="My Block Extension">

<s-form

onSubmit={(event) => {

event.waitUntil(fetch('app:data/save'));

console.log('submit', {textValue, numberValue});

}

onReset={() => console.log('automatically reset values')}

>

<s-stack direction="block" gap="base">

<s-text-field

label="Default Value"

name="my-text"

value={textValue}

onChange={(e) => setTextValue(e.currentTarget.value)}

/>

<s-number-field

label="Percentage field"

name="my-number"

value={numberValue}

onChange={(e) => setNumberValue(e.currentTarget.value)}

/>

</s-stack>

</s-form>

</s-admin-block>

);

}

```

## [Anchor to Picking resources](/docs/api/admin-extensions/latest/index#picking-resources)Picking resourcesUse the Resource Picker and Picker API's to allow users to select resources for your extension to use.Resource Picker

Use the `resourcePicker` API to display a search-based interface to help users find and select one or more products, collections, or product variants, and then return the selected resources to your extension. Both the app and the user must have the necessary permissions to access the resources selected.Picker

Use the `picker` API to display a search-based interface to help users find and select one or more custom data types that you provide, such as product reviews, email templates, or subscription options.## resourcePickerCopy## Selecting a product99123456789101112131415import { render } from 'preact';export default async () => {  render(<Extension />, document.body);}function Extension() {  const handleSelectProduct = async () => {    const selected = await shopify.resourcePicker({ type: 'product' });    console.log(selected);  };  return <s-button onClick={handleSelectProduct}>Select product</s-button>;}## pickerCopy## Selecting an email template991234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950import { render } from 'preact';export default async () => {  render(<Extension />, document.body);}function Extension() {  const handleSelectEmailTemplate = async () => {    const pickerInstance = await shopify.picker({      heading: 'Select a template',      multiple: false,      headers: [        { content: 'Templates' },        { content: 'Created by' },        { content: 'Times used', type: 'number' },      ],      items: [        {          id: '1',          heading: 'Full width, 1 column',          data: ['Karine Ruby', '0'],          badges: [{ content: 'Draft', tone: 'info' }, { content: 'Marketing' }],        },        {          id: '2',          heading: 'Large graphic, 3 column',          data: ['Charlie Mitchell', '5'],          badges: [            { content: 'Published', tone: 'success' },            { content: 'New feature' },          ],          selected: true,        },        {          id: '3',          heading: 'Promo header, 2 column',          data: ['Russell Winfield', '10'],          badges: [{ content: 'Published', tone: 'success' }],        },      ],    });    const selected = await pickerInstance.selected;    console.log(selected);  };  return (    <s-button onClick={handleSelectEmailTemplate}>Select email template</s-button>  );}

## [Anchor to Deploying](/docs/api/admin-extensions/latest/index#deploying)DeployingUse the Shopify CLI to [deploy your app and its extensions](/docs/apps/deployment/extension).## Deploy an extensionCopy## CLI91234567# navigate to your app's root directory:cd my-app# deploy your app and its extensions:shopify app deploy# follow the steps to deploy

## [Anchor to Tutorials and resources](/docs/api/admin-extensions/latest/index#tutorials-and-resources)Tutorials and resourcesDeepen your understanding of Admin UI extensions with these tutorials and resources.[TutorialGet started building your first admin extensionTutorialGet started building your first admin extension](/docs/apps/admin/admin-actions-and-blocks/build-an-admin-action)[Tutorial - Get started building your first admin extension](/docs/apps/admin/admin-actions-and-blocks/build-an-admin-action)[Component APIsSee all available componentsComponent APIsSee all available components](/docs/api/admin-extensions/components)[Component APIs - See all available components](/docs/api/admin-extensions/components)[ReferenceView a list of available extension targetsReferenceView a list of available extension targets](/docs/api/admin-extensions/2026-01/extension-targets)[Reference - View a list of available extension targets](/docs/api/admin-extensions/2026-01/extension-targets)[Network featuresLearn about the network features available to admin extensionsNetwork featuresLearn about the network features available to admin extensions](/docs/api/admin-extensions/2026-01/network-features)[Network features - Learn about the network features available to admin extensions](/docs/api/admin-extensions/2026-01/network-features)[Using formsUse the Form component to integrate with the contextual save bar of the resource pageUsing formsUse the Form component to integrate with the contextual save bar of the resource page](/docs/api/admin-extensions/latest/#using-forms)[Using forms - Use the Form component to integrate with the contextual save bar of the resource page](#using-forms)[Picking resourcesPrompt the user to select resourcesPicking resourcesPrompt the user to select resources](/docs/api/admin-extensions/latest/#picking-resources)[Picking resources - Prompt the user to select resources](#picking-resources)[Figma kitUse the Figma kit to design your extensionFigma kitUse the Figma kit to design your extension](https://www.figma.com/community/file/1554895871000783188/polaris-ui-kit-community)[Figma kit - Use the Figma kit to design your extension](https://www.figma.com/community/file/1554895871000783188/polaris-ui-kit-community)

Was this page helpful?YesNo### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)