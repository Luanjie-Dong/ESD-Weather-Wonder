"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Bell, Home, MapPin, Settings } from "lucide-react"
import { cn } from "@/lib/utils"

export default function Navbar() {
  const pathname = usePathname()

  const navItems = [
    { href: "/dashboard", label: "Home", icon: Home },
    { href: "/locations", label: "Locations", icon: MapPin },
    { href: "/alerts", label: "Alerts", icon: Bell },
    { href: "/settings", label: "Settings", icon: Settings },
  ]

  return (
    <nav className="fixed bottom-0 left-0 z-50 w-full border-t border-border bg-background md:relative md:border-b md:border-t-0">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/dashboard" className="hidden items-center gap-2 md:flex">
          <span className="text-xl font-bold text-brand">Weather Wonder</span>
        </Link>

        <div className="flex w-full items-center justify-around md:w-auto md:justify-end md:gap-6">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex flex-col items-center justify-center gap-1 p-1.5 text-sm transition-colors md:flex-row md:gap-2",
                  isActive ? "text-brand" : "text-muted-foreground hover:text-foreground",
                )}
              >
                <Icon className="h-5 w-5" />
                <span className="md:text-base">{item.label}</span>
              </Link>
            )
          })}
        </div>
      </div>
    </nav>
  )
}

