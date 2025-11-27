import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { ThemeProvider } from "@/components/theme-provider"
import { TooltipProvider } from "@/components/ui/tooltip"
import { DashboardLayout } from "@/components/dashboard-layout"

// Pages
import DashboardPage from "@/pages/dashboard"
import DevicesPage from "@/pages/devices"
import AnalyticsPage from "@/pages/analytics"
import EnergyPage from "@/pages/energy"
import BatteryPage from "@/pages/battery"
import UsersPage from "@/pages/users"
import AlertsPage from "@/pages/alerts"
import SettingsPage from "@/pages/settings"
import LoginPage from "@/pages/login"

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="solarhub-theme">
      <TooltipProvider>
        <BrowserRouter>
          <Routes>
            {/* Auth routes */}
            <Route path="/login" element={<LoginPage />} />

            {/* Dashboard routes */}
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/devices" element={<DevicesPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/energy" element={<EnergyPage />} />
              <Route path="/battery" element={<BatteryPage />} />
              <Route path="/users" element={<UsersPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>

            {/* Redirect root to dashboard */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Catch all - redirect to dashboard */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ThemeProvider>
  )
}

export default App
