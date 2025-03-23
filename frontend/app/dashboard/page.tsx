import AuthCheck from "../components/auth-check"
import DashboardContent from "../components/dashboard-content"

export default function DashboardPage() {
  return (
    <AuthCheck>
      <DashboardContent />
    </AuthCheck>
  )
}