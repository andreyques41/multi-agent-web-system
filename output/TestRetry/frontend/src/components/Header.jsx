import React from 'react';

const Header = () => {
    return (
        <header className="bg-blue-800 text-white py-4">
            <div className="container mx-auto flex justify-between items-center">
                <h1 className="text-xl font-bold">TestRetry</h1>
                <nav>
                    <ul className="flex space-x-4">
                        <li><a href="#home" className="hover:underline">Home</a></li>
                        <li><a href="#features" className="hover:underline">Features</a></li>
                        <li><a href="#contact" className="hover:underline">Contact</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
};

export default Header;