"use client"
import { Button } from "@/components/ui/button"
import { logout } from "@/app/lib/auth"
import { useRouter } from "next/navigation"
import Navbar from "@/components/navbar"
import AuthCheck from "@/components/auth-check"

export default function DashboardPage() {
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.push("/")
  }
  
  return (
    <AuthCheck>
      <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 pb-16 pt-6 md:pb-6">
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold md:text-3xl">Welcome back, Alex</h1>
            <Button variant="outline" size="sm" onClick={handleLogout}>
              Log Out
            </Button>
          </div>

          {/* Rest of your dashboard content */}
          {/* Copy the content from your original home page here */}
        </div>
      </main>
    </div>
  </AuthCheck>
  )
}