---
{
  "fetch": {
    "url": "https://shopify.dev/api/app-bridge/using-modals-in-your-app",
    "fetched_at": "2026-02-10T13:39:57.585201",
    "status": 200,
    "size_bytes": 433616
  },
  "metadata": {
    "title": "Using modals in your app",
    "source": "shopify",
    "category": "polaris-web-components",
    "section": "app-bridge",
    "component": "using-modals-in-your-app"
  }
}
---

# Using modals in your app

ExpandOn this page- [Why App Bridge Modals instead of Polaris React Modals](/docs/api/app-bridge/using-modals-in-your-app#why-app-bridge-modals-instead-of-polaris-react-modals)- [How App Bridge modals work](/docs/api/app-bridge/using-modals-in-your-app#how-app-bridge-modals-work)- [Modals with HTML content](/docs/api/app-bridge/using-modals-in-your-app#modals-with-html-content)- [Modals with a route](/docs/api/app-bridge/using-modals-in-your-app#modals-with-a-route)- [FAQ](/docs/api/app-bridge/using-modals-in-your-app#faq)

# Using modals in your appAsk assistantModals are overlays that require merchants to take an action before they can continue interacting with the rest of Shopify. They can be disruptive and should be used thoughtfully and sparingly.If you need to use a modal in your app or have some questions about how App Bridge modals work, then you can follow this guide to understand how and when to use them.As a rule of thumb, complex use cases should use the [src](/docs/api/app-home/web-components/ui-modal#uimodalelement-propertydetail-src) attribute to render a route while simple content can use [HTML children](/docs/api/app-home/web-components/ui-modal#uimodalelement-propertydetail-children) in the modal body. Refer to the table below for some sample use cases and which type of modal you would use to achieve them.| Use case | Modal type || A confirmation dialog with a simple string for content | HTML content || A form with a few fields and buttons to cancel or submit | HTML content || A video taking up the full width and height | HTML content || A form that uses components like the Polaris React Popover and Tooltip | both, [with caveats](#react-components-using-react-portals) || A list that can be rearranged by dragging and dropping items | src attribute || A canvas editor used to create an email template | src attribute |For specific information on max modal usage, refer to the [App Design Guidelines](/docs/apps/design/app-structure#max-modal).

## [Anchor to Why App Bridge Modals instead of Polaris React Modals](/docs/api/app-bridge/using-modals-in-your-app#why-app-bridge-modals-instead-of-polaris-react-modals)Why App Bridge Modals instead of Polaris React ModalsYou may have reached this guide after seeing that the [Polaris Modal](https://polaris-react.shopify.com/components/deprecated/modal) has been deprecated. There are a few key reasons that we recommend using App Bridge modals instead of Polaris React Modals.### [Anchor to Centering in the Shopify admin](/docs/api/app-bridge/using-modals-in-your-app#centering-in-the-shopify-admin)Centering in the Shopify adminModals are used across the Shopify admin. They are centered in the page with a background overlay obscuring the sidebar and top bar.When you use a Polaris React modal inside of your app, it's rendered directly in the app and centered in the app frame, since the app frame deos not span the whole space of the Shopify admin. The app frame behind the modal is greyed out but the side bar and top bar of the Shopify admin remain unchanged:When you use an App Bridge modal inside of your app, it's rendered outside of the app frame in the Shopify admin and centered in the page. The entire Shopify admin, including the sidebar and top bar, are greyed out:### [Anchor to Standardized modal header and footer](/docs/api/app-bridge/using-modals-in-your-app#standardized-modal-header-and-footer)Standardized modal header and footerAnother aspect of visual consistency is the modal header and footer. In order to maintain that consistency, we control the rendering of the modal header and footer inside the Shopify admin and put constraints around the components rendered inside of it.### [Anchor to Automatic updates](/docs/api/app-bridge/using-modals-in-your-app#automatic-updates)Automatic updatesPolaris React is versioned. Its code is bundled into your app code. If you don't keep up to date with the latest versions, then the styling can quickly become out of sync with the rest of the Shopify admin. The code for App Bridge modals is loaded from a CDN and Shopify regularily updates it. As such, you don't need to worry about dependency updates because Shopify will keep App Bridge modals up to date with the rest of the Shopify admin.

## [Anchor to How App Bridge modals work](/docs/api/app-bridge/using-modals-in-your-app#how-app-bridge-modals-work)How App Bridge modals workApp Bridge modals are different than other modals you may have used, such as the now-deprecated [Polaris React Modal](https://polaris-react.shopify.com/components/deprecated/modal).To center the modal in the Shopify admin and control the layout of the modal header and footer, modals are rendered by the Shopify admin rather than directly in your app. To center a modal, we render a modal and create an `iframe` inside of it that is same-origin to your app. This `iframe` is then used to either load the custom HTML content you provide or the `src` URL for a route in your app.

## [Anchor to Modals with HTML content](/docs/api/app-bridge/using-modals-in-your-app#modals-with-html-content)Modals with HTML contentModals can be created with simple HTML elements as content.HTMLReactCopy91234<ui-modal id="my-modal">  <p>This is my modal message.</p>  <ui-title-bar title="Title"></ui-title-bar></ui-modal>991234567891011import {Modal, TitleBar} from '@shopify/app-bridge-react';import {Text} from '@shopify/polaris';function MyModal() {  return (    <Modal id="my-modal">      <Text as="p">This is my modal message.</Text>      <TitleBar title="Title"></TitleBar>    </Modal>  )}HTML```

<ui-modal id="my-modal">

<p>This is my modal message.</p>

<ui-title-bar title="Title"></ui-title-bar>

</ui-modal>

```React```

import {Modal, TitleBar} from '@shopify/app-bridge-react';

import {Text} from '@shopify/polaris';

function MyModal() {

return (

<Modal id="my-modal">

<Text as="p">This is my modal message.</Text>

<TitleBar title="Title"></TitleBar>

</Modal>

)

}

```For more information on usage, refer to the [`ui-modal` component](/docs/api/app-home/web-components/ui-modal). When you open a modal with HTML content, App Bridge moves this content into the modal's `iframe`. It also copies the stylesheets from your app into the modal frame to ensure your modal styles match your app styles.These modals are meant to be used for simple use cases. Go to the [Examples](#examples) section to see some common use cases and the [Limitations](#limitations) section to learn about what can't be done using these modals.You can only provide a single parent element, commonly a `p`, `form`, or a `div`. This is because App Bridge needs a single DOM element to search for when moving the content into the modal frame.### [Anchor to React components](/docs/api/app-bridge/using-modals-in-your-app#react-components)React componentsWe provide the [`@shopify/app-bridge-react`](https://www.npmjs.com/package/@shopify/app-bridge-react) library that contains React wrappers for App Bridge components, such as the [Modal React component](/docs/api/app-home/react-components/modal). Using this component has an added benefit that you are not limited to a single parent element like you are when using standard HTML content. This package is versioned for API updates but will still receives automatic updates to things like modal styling as it relies on the App Bridge script from the Shopify CDN.## index.jsxCopy99123456789101112import {Modal, TitleBar} from '@shopify/app-bridge-react';import {Text} from '@shopify/polaris';function MyModal() {  return (    <Modal id="my-modal">      <Text as="p">This is the first modal message.</Text>      <Text as="p">This is the second modal message.</Text>      <TitleBar title="Title"></TitleBar>    </Modal>  )}If you don't use the Shopify App Bridge React package, then you'll need to set up a [React portal](https://react.dev/reference/react-dom/createPortal) for the React components inside of your modal as they're rendered in a different part of the DOM. We recommend you use the [Modal React component](/docs/api/app-home/react-components/modal) to avoid this complexity, as it sets this up for you.### [Anchor to Examples](/docs/api/app-bridge/using-modals-in-your-app#examples)ExamplesYou can use a modal with custom content to achieve any of the following examples:

- [Simple message modal](#simple-message-modal)

- [Simple form](#simple-form)

#### [Anchor to Simple message modal](/docs/api/app-bridge/using-modals-in-your-app#simple-message-modal)Simple message modalYou might use an HTML content modal to show a confirmation dialog for a destructive action. You can provide a simple message string in a `p` element and buttons to control deleting and cancelling.HTMLReactCopy9123456789<ui-modal id="confirmation-modal">  <p>If you delete this resource, it can't be undone.</p>  <ui-title-bar title="Delete this resource">    <button variant="primary" tone="critical" onclick="console.log('Deleting')">      Delete    </button>    <button onclick="console.log('Cancelling')">Cancel</button>  </ui-title-bar></ui-modal>99123456789101112131415import {Modal, TitleBar} from '@shopify/app-bridge-react';import {Text} from '@shopify/polaris';function MyModal() {  return (    <Modal id="confirmation-modal">      <Text as="p">If you delete this resource, it can't be undone.</Text>      <TitleBar title="Delete this resource">        <button variant="primary" tone="critical" onClick={() => console.log("Deleting")}>          Delete        </button>      </TitleBar>    </Modal>  )}HTML```

<ui-modal id="confirmation-modal">

<p>If you delete this resource, it can't be undone.</p>

<ui-title-bar title="Delete this resource">

<button variant="primary" tone="critical" onclick="console.log('Deleting')">

Delete

</button>

<button onclick="console.log('Cancelling')">Cancel</button>

</ui-title-bar>

</ui-modal>

```React```

import {Modal, TitleBar} from '@shopify/app-bridge-react';

import {Text} from '@shopify/polaris';

function MyModal() {

return (

<Modal id="confirmation-modal">

<Text as="p">If you delete this resource, it can't be undone.</Text>

<TitleBar title="Delete this resource">

<button variant="primary" tone="critical" onClick={() => console.log("Deleting")}>

Delete

</button>

</TitleBar>

</Modal>

)

}

```#### [Anchor to Simple form](/docs/api/app-bridge/using-modals-in-your-app#simple-form)Simple formYou might use an HTML content modal to present a simple form to the merchant. You can provide the form inputs inside of a `form` element and use the `data-save-bar` attribute to connect with the contextual save bar in the Shopify admin.HTMLReactCopy9912345678910111213<ui-modal id="name-modal" variant="max">  <form data-save-bar>    <label>      Name:      <input name="submitted-name" autocomplete="name" />    </label>    <button>Save</button>  </form>  <ui-title-bar title="Register">    <button variant="primary">Save</button>    <button>Cancel</button>  </ui-title-bar></ui-modal>991234567891011121314151617181920212223242526272829import {Modal, TitleBar} from '@shopify/app-bridge-react';import {TextField} from '@shopify/polaris';import {useState, useCallback} from 'react';function MyModal() {  const [value, setValue] = useState('');  const handleChange = useCallback(    (newValue: string) => setValue(newValue),    [],  );  return (    <Modal id="name-modal">      <form data-save-bar>        <TextField          label="Name:"          value={value}          onChange={handleChange}          autoComplete="name"        />      </form>      <TitleBar title="Register">        <button variant="primary">Save</button>        <button>Cancel</button>      </TitleBar>    </Modal>  )}HTML```

<ui-modal id="name-modal" variant="max">

<form data-save-bar>

<label>

Name:

<input name="submitted-name" autocomplete="name" />

</label>

<button>Save</button>

</form>

<ui-title-bar title="Register">

<button variant="primary">Save</button>

<button>Cancel</button>

</ui-title-bar>

</ui-modal>

```React```

import {Modal, TitleBar} from '@shopify/app-bridge-react';

import {TextField} from '@shopify/polaris';

import {useState, useCallback} from 'react';

function MyModal() {

const [value, setValue] = useState('');

const handleChange = useCallback(

(newValue: string) => setValue(newValue),

[],

);

return (

<Modal id="name-modal">

<form data-save-bar>

<TextField

label="Name:"

value={value}

onChange={handleChange}

autoComplete="name"

/>

</form>

<TitleBar title="Register">

<button variant="primary">Save</button>

<button>Cancel</button>

</TitleBar>

</Modal>

)

}

```### [Anchor to Limitations](/docs/api/app-bridge/using-modals-in-your-app#limitations)LimitationsApp Bridge is moving the HTML content you provide in the `ui-modal` element into the `iframe` created in the modal in the Shopify admin.If you require any of the functionality listed in these limitations, then we recommend using the `src` modal explained in the [Modals with a route](#modals-with-a-route) section.#### [Anchor to JavaScript loading](/docs/api/app-bridge/using-modals-in-your-app#javascript-loading)JavaScript loadingApp Bridge only copies the HTML elements and stylesheets into the modal frame. Custom JavaScript and `template` tags that you rely on in your app are not copied.#### [Anchor to document access](/docs/api/app-bridge/using-modals-in-your-app#document-access)document accessAs the modal is rendered in a different frame, you do not have direct access to the `document`. Some [npm](https://www.npmjs.com/) libraries are incompatible with this approach, such as commonly used drag-and-drop libraries.#### [Anchor to React components using React Portals](/docs/api/app-bridge/using-modals-in-your-app#react-components-using-react-portals)React components using React PortalsUsing React portals for custom React content is a requirement. When using [Polaris](https://polaris.shopify.com/) components built with React Portals, like `Popover`, `Tooltip`, and `Combobox` in a modal, you must wrap your modal's child components in a [Polaris App Provider](https://polaris.shopify.com/components/utilities/app-provider).## index.jsxCopy9912345678910111213141516171819import {Modal, TitleBar} from '@shopify/app-bridge-react';import {ActionList, AppProvider, Popover} from '@shopify/polaris';function MyModal() {  return (    <Modal id="my-modal">      <AppProvider i18n={{}}>        <Popover          active="true"          activator={(<Button>More Actions</Button>)}          onClose={() => {}}        >          <ActionList items={[{content: 'Action 1'}, {content: 'Action 2'}]}/>        </Popover>      </AppProvider>      <TitleBar title="Title"></TitleBar>    </Modal>  )}NoteYou must be using Polaris 13.19.x or higher for the Polaris App Provider to contextualize components built with React Portals**Note:** You must be using Polaris 13.19.x or higher for the Polaris App Provider to contextualize components built with React Portals

## [Anchor to Modals with a route](/docs/api/app-bridge/using-modals-in-your-app#modals-with-a-route)Modals with a routeModals can be created with a `src` attribute that accepts a same-origin URL to load in the modal frame.## index.htmlCopy912345678<ui-modal id="my-modal" src="/modal-route">  <ui-title-bar title="Title">    <button variant="primary">Label</button>    <button onclick="document.getElementById('my-modal').hide()">Label</button>  </ui-title-bar></ui-modal><button onclick="document.getElementById('my-modal').show()">Open Modal</button>## modal-route.htmlCopy9912345678910111213<!DOCTYPE html><html>  <head>    <meta charset="utf-8" />    <meta name="viewport" content="width=device-width, initial-scale=1" />    <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />    <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>  </head>  <body>    <h1>My separate route</h1>  </body></html>When you open a modal with the `src` attribute, App Bridge uses this URL as the iframe's `src` attribute. You will need to setup a route in your app to be used within the modal. Modals rendering a route via the `src` attribute are the recommend path for rendering complex content or functionality requiring 3rd-party libraries.NoteYou need to add the `app-bridge.js` script tag, along with any CSS or JS assets you need to any modal routes that you use within your app.**Note:** You need to add the `app-bridge.js` script tag, along with any CSS or JS assets you need to any modal routes that you use within your app.### [Anchor to How to communicate with your main app frame](/docs/api/app-bridge/using-modals-in-your-app#how-to-communicate-with-your-main-app-frame)How to communicate with your main app frameOne complexity that come with loading a modal `iframe` within an app `iframe` is communication between the two frames. You can use the [postMessage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) to communicate with the parent page from within your modal. You can access `postMessage` through the `window.opener` object in the modal and through the `modal.contentWindow` object in the parent page.## main-app.jsxCopy9912345678910111213141516171819202122232425262728293031import {Modal, useAppBridge} from '@shopify/app-bridge-react';function MyApp() {  const app = useAppBridge();  const [modalOpen, setModalOpen] = useState(false);  useEffect(() => {    function handleMessageFromModal(ev) {      console.log('Message received in main app:', ev.data);    }    window.addEventListener('message', handleMessageFromModal)    return () => {      window.removeEventListener('message', handleMessageFromModal)    }  }, [])  const sendMessageToApp = () => {    const modal = document.getElementById('my-modal');    modal.contentWindow.postMessage('Hi, this is the main app!', location.origin);  }  return (    <div>      <Modal id="my-modal" src="/modal-route" open={modalOpen}>        <TitleBar title="Hello world!" />      </Modal>      <button onClick={() => setModalOpen(true)}>Open modal</button>    </div>  )}## modal-route.jsxCopy9912345678910111213141516171819202122232425262728import {useAppBridge} from '@shopify/app-bridge-react';// configure route with app-bridge.js script tag herefunction ModalRouteComponent() {  const app = useAppBridge();  useEffect(() => {    function handleMessageFromMainApp(ev) {      console.log('Message received in modal:', ev.data);    }    window.addEventListener('message', handleMessageFromMainApp)    return () => {      window.removeEventListener('message', handleMessageFromMainApp)    }  }, [])  const sendMessageToApp = () => {    window.opener.postMessage('Hi, this is the modal!', location.origin);  }  return (    <div>      <button onClick={sendMessageToApp}>Send message</button>    </div>  )}### [Anchor to Limitations](/docs/api/app-bridge/using-modals-in-your-app#limitations)LimitationsModals are meant to be used as presentation layers for specific use cases. As such, the available features inside of the modal frame are limited. You're not able to access App Bridge features such as [toast](/docs/api/app-home/apis/toast) directly in your modal. Instead, you should communicate with your main app frame to share state and use App Bridge features.You're only able to access the [environment](/docs/api/app-home/apis/environment) feature directly from within your modal.

## [Anchor to FAQ](/docs/api/app-bridge/using-modals-in-your-app#faq)FAQThis section provides answers to some commonly asked questions about App Bridge modals.### [Anchor to Why do Polaris components like Popover, Tooltip, and Combobox render outside of my modal?](/docs/api/app-bridge/using-modals-in-your-app#why-do-polaris-components-like-popover-tooltip-and-combobox-render-outside-of-my-modal)Why do Polaris components like Popover, Tooltip, and Combobox render outside of my modal?The App Bridge React Modal component creates a [React portal](https://react.dev/reference/react-dom/createPortal) for you so that you can use React components in your simple HTML content modal. If you are using Polaris components built with React Portals, you must wrap the modal's children in a [Polaris App Provider](https://polaris.shopify.com/components/utilities/app-provider). Alternatively, you can use the `src` modal.### [Anchor to How can I access my main app context from within my src modal?](/docs/api/app-bridge/using-modals-in-your-app#how-can-i-access-my-main-app-context-from-within-my-src-modal)How can I access my main app context from within my src modal?You can use the [window.opener](https://developer.mozilla.org/en-US/docs/Web/API/Window/opener) property to get a reference to the main app frame window. This can be helpful when communicating state between the frames, be it through `postMessage` or another method.### [Anchor to Do I have to do anything different for mobile?](/docs/api/app-bridge/using-modals-in-your-app#do-i-have-to-do-anything-different-for-mobile)Do I have to do anything different for mobile?No, App Bridge modals work the same in mobile and desktop views.### [Anchor to I'm trying to use a 3rd-party library inside of my modal but it's not working. What do I do?](/docs/api/app-bridge/using-modals-in-your-app#im-trying-to-use-a-3rd-party-library-inside-of-my-modal-but-its-not-working-what-do-i-do)I'm trying to use a 3rd-party library inside of my modal but it's not working. What do I do?3rd-party libraries, such as drag-and-drop libraries, may be accessing the `document` or be otherwise incompatible with custom content modals. You should set up a route in your app for the modal content and use the [src](/docs/api/app-home/web-components/ui-modal#uimodalelement-propertydetail-src) modal for use cases like this.### [Anchor to I'm trying to use a src modal but I'm not seeing the same CSS and JS as my app. Do I have to include these myself?](/docs/api/app-bridge/using-modals-in-your-app#im-trying-to-use-a-src-modal-but-im-not-seeing-the-same-css-and-js-as-my-app-do-i-have-to-include-these-myself)I'm trying to use a src modal but I'm not seeing the same CSS and JS as my app. Do I have to include these myself?Yes, you need to reinclude any CSS and JS that you need on this page, since it's a separate page loaded in a separate iframe from your main app.

Was this page helpful?YesNo- [Why App Bridge Modals instead of Polaris React Modals](/docs/api/app-bridge/using-modals-in-your-app#why-app-bridge-modals-instead-of-polaris-react-modals)- [How App Bridge modals work](/docs/api/app-bridge/using-modals-in-your-app#how-app-bridge-modals-work)- [Modals with HTML content](/docs/api/app-bridge/using-modals-in-your-app#modals-with-html-content)- [Modals with a route](/docs/api/app-bridge/using-modals-in-your-app#modals-with-a-route)- [FAQ](/docs/api/app-bridge/using-modals-in-your-app#faq)### Updates- [Developer changelog](/changelog)- [Shopify Editions](https://www.shopify.com/editions)### Business growth- [Shopify Partners Program](https://www.shopify.com/partners?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify App Store](https://apps.shopify.com/?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Academy](https://www.shopifyacademy.com/page/catalog#role_developer?utm_source=web_dotdev&utm_medium=footer_businessgrowth)### Legal- [Terms of service](https://www.shopify.com/legal/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [API terms of use](https://www.shopify.com/legal/api-terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Privacy policy](https://www.shopify.com/legal/privacy?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Partners Program Agreement](https://www.shopify.com/partners/terms?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)### Shopify- [About Shopify](https://www.shopify.com/about?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Shopify Plus](https://www.shopify.com/plus?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Careers](https://www.shopify.com/careers?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Investors](https://investors.shopify.com/home/default.aspx?shpxid=222dd762-CA08-48FF-E4D4-FF926B8FFCAD)- [Press and media](https://shopify.com/news?shpxid=7db0d4e4-24E8-4087-58FA-7EE470CA745A)