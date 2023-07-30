import "./globals.css";
import "./force.css";

import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: 'RescueRepo',
  description: 'Resurrecting old abandonware repos, and reducing the effort to get them up and running again.',
  keywords: [
    'ai',
    'ml',
    'machine-learning',
    'artificial-intelligence',
    'biology',
    'bioinformatics',
    'abandonware',
    'github',
    'protein',
    'protein-folding',
    'nextflow',
    'redun',
    'flyte',
    'nextjs',
    'fastapi',
    'openai',
    'anthropic',
    'langchain',
    'rlhf',
    'gpt4',
    'gpt-4',
    'gpt3',
    'gpt-3',
    'chatgpt',
    'chat-gpt',
    'claude',
  ],
  authors: [
    {
      name: 'RescueRepo',
      url: 'https://github.com/matthew-mcateer/rescuerepo',
    },
  ],
  creator: 'RescueRepo',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: 'white' },
    { media: '(prefers-color-scheme: dark)', color: 'black' },
  ],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://github.com/matthew-mcateer/rescuerepo',
    siteName: 'RescueRepo',
  },
  twitter: {
    card: 'summary_large_image.png',
    images: [`og.jpg`],
    creator: `@matthewmcateer0`,
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={inter.className}
        style={{
          backgroundImage: `url("https://matthewmcateer.me/media/image-sizing-post/plain_dark_background_bc5035f2-16e6-429c-9408-f0e497cebbd1.png")`,
          backgroundSize: "100%",
          backgroundPosition: "right 0px top 0px",
          backgroundRepeat: "no-repeat",
          backgroundColor: "#000",
        }}
      >
        {children}
      </body>
    </html>
  );
}
