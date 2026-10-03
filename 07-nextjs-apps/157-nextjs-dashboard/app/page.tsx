import StatsCard from "@/components/StatsCard";
import Card from "@/components/Card";
import DataTable from "@/components/DataTable";
import {
  DollarSign,
  Users,
  ShoppingCart,
  TrendingUp,
} from "lucide-react";

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400">Welcome back! Here's an overview of your metrics.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Revenue"
          value="$45,231"
          change="+12.5%"
          changeType="positive"
          icon={<DollarSign className="w-5 h-5" />}
        />
        <StatsCard
          title="Total Users"
          value="2,350"
          change="+4.2%"
          changeType="positive"
          icon={<Users className="w-5 h-5" />}
        />
        <StatsCard
          title="Orders"
          value="1,234"
          change="-2.1%"
          changeType="negative"
          icon={<ShoppingCart className="w-5 h-5" />}
        />
        <StatsCard
          title="Growth"
          value="+18.7%"
          change="+8.3%"
          changeType="positive"
          icon={<TrendingUp className="w-5 h-5" />}
        />
      </div>

      {/* Charts and Tables */}
      <div className="grid lg:grid-cols-2 gap-6">
        <Card title="Revenue Overview">
          <div className="h-64 flex items-center justify-center bg-gray-800/50 rounded-lg">
            <div className="text-center">
              <div className="text-6xl font-bold text-white mb-2">$45,231</div>
              <div className="text-gray-400">Monthly revenue chart placeholder</div>
            </div>
          </div>
        </Card>
        <Card title="User Activity">
          <div className="h-64 flex items-center justify-center bg-gray-800/50 rounded-lg">
            <div className="text-center">
              <div className="text-6xl font-bold text-white mb-2">2,350</div>
              <div className="text-gray-400">Active users this month</div>
            </div>
          </div>
        </Card>
      </div>

      {/* Data Table */}
      <Card title="Recent Orders">
        <DataTable />
      </Card>
    </div>
  );
}
