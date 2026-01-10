import "@/styles/globals.css"
import type {AppProps} from "next/app"

/**
 * Next.js Pages Router, _app.tsx 是所有页面的根组件
 * @param Component 当前要渲染的页面组件
 * @param pageProps 页面接收的 props
 * @constructor
 */
export default function App({Component, pageProps}: AppProps) {
    return <Component {...pageProps} />
}

