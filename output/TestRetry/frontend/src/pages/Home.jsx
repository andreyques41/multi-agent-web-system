import React from 'react';

const Home = () => {
    return (
        <section id="home" className="bg-gray-100 py-16">
            <div className="container mx-auto text-center">
                <h2 className="text-3xl font-bold mb-4">Welcome to TestRetry</h2>
                <p className="mb-8">Streamline your business processes with our cutting-edge solutions.</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="p-4 bg-white shadow-md rounded">
                        <h3 className="text-xl font-semibold mb-2">Feature 1</h3>
                        <p>Optimize your workflows effortlessly.</p>
                    </div>
                    <div className="p-4 bg-white shadow-md rounded">
                        <h3 className="text-xl font-semibold mb-2">Feature 2</h3>
                        <p>Gain actionable insights with analytics.</p>
                    </div>
                    <div className="p-4 bg-white shadow-md rounded">
                        <h3 className="text-xl font-semibold mb-2">Feature 3</h3>
                        <p>Secure and reliable user management.</p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Home;