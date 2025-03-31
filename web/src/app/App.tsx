import { Dropdown } from '../components/Dropdown'

export function App() {
    return (
        <div className="min-h-screen bg-gray-100">
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                    <h1 className="text-3xl font-bold text-gray-900">D&D Simulator</h1>
                </div>
            </header>
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <div className="px-4 py-6 sm:px-0">
                    <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
                        <p className="text-xl text-gray-500">Welcome to the D&D Simulator!</p>
                    </div>
                </div>
                <div className="flex flex-col gap-4 max-w-xl">
                    <Dropdown title="Dropdown">
                        <div>Hello</div>
                    </Dropdown>
                </div>
            </main>
        </div>
    )
}
