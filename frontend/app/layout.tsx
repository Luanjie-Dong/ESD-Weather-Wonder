import type React from "react"
import type { Metadata } from "next"
import { Lato } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"

const lato = Lato({
  subsets: ["latin"],
  weight: ["100", "300", "400", "700", "900"],
  variable: "--font-lato",
})

export const metadata: Metadata = {
  title: "Weather Alert App",
  description: "Modern weather forecasting and alert system",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${lato.variable} font-sans`}>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}



import './globals.css'