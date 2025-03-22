import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import Link from "next/link"
import { CloudLightning } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-border">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <CloudLightning className="h-6 w-6 text-brand" />
            <span className="text-xl font-bold text-brand">WeatherAlert</span>
          </div>
          <Button asChild variant="outline">
            <Link href="/landing?tab=login">Sign In</Link>
          </Button>
        </div>
      </header>

      <main className="flex-1">
        <div className="container grid items-center gap-6 pb-8 pt-6 md:grid-cols-2 md:py-10">
          <div className="flex flex-col justify-center space-y-4">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Stay ahead of the weather</h1>
              <p className="text-muted-foreground md:text-xl">
                Get real-time weather updates and emergency alerts for your favorite locations.
              </p>
            </div>

            <div className="flex flex-col gap-2 sm:flex-row">
              <Button size="lg" asChild>
                <Link href="/landing?tab=signup">Get Started</Link>
              </Button>
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </div>

            <div className="mt-4 grid grid-cols-3 gap-2 text-center">
              <div className="rounded-lg bg-muted p-2">
                <p className="text-2xl font-bold">100+</p>
                <p className="text-xs text-muted-foreground">Countries</p>
              </div>
              <div className="rounded-lg bg-muted p-2">
                <p className="text-2xl font-bold">10K+</p>
                <p className="text-xs text-muted-foreground">Cities</p>
              </div>
              <div className="rounded-lg bg-muted p-2">
                <p className="text-2xl font-bold">24/7</p>
                <p className="text-xs text-muted-foreground">Alerts</p>
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <Tabs defaultValue="signup" className="w-full max-w-md">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="signup">Sign Up</TabsTrigger>
                <TabsTrigger value="login">Log In</TabsTrigger>
              </TabsList>

              <TabsContent value="signup" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Create an account</CardTitle>
                    <CardDescription>Enter your information to create an account</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Name</Label>
                      <Input id="name" placeholder="John Doe" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input id="email" type="email" placeholder="john@example.com" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <Input id="password" type="password" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="location">Default Location</Label>
                      <Input id="location" placeholder="City, State" />
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button className="w-full">Create Account</Button>
                  </CardFooter>
                </Card>
              </TabsContent>

              <TabsContent value="login" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Log in</CardTitle>
                    <CardDescription>Enter your credentials to access your account</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="login-email">Email</Label>
                      <Input id="login-email" type="email" placeholder="john@example.com" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="login-password">Password</Label>
                      <Input id="login-password" type="password" />
                    </div>
                  </CardContent>
                  <CardFooter className="flex flex-col space-y-2">
                    <Button className="w-full" asChild>
                      <Link href="/">Log In</Link>
                    </Button>
                    <Button variant="link" size="sm" className="w-full">
                      Forgot password?
                    </Button>
                  </CardFooter>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </main>
    </div>
  )
}

