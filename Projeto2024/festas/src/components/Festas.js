import React, { useState, useEffect, useRef } from 'react';
import Festa from './Festa'; 
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const Festas = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [showFilters, setShowFilters] = useState(false);
    const [containerHeight, setContainerHeight] = useState(0);
    const [festas, setFestas] = useState([]);

    const headerRef = useRef(null);

    useEffect(() => {
        const handleResize = () => {
            const headerHeight = headerRef.current ? headerRef.current.offsetHeight : 0;
            setContainerHeight(window.innerHeight * 0.75 - headerHeight);
        };

        handleResize();
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    useEffect(() => {
        const fetchFestas = async () => {
            try {
                const response = await fetch('http://localhost:5000/festas');
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                const data = await response.json();
                setFestas(data); // Directly set the fetched data to state
            } catch (error) {
                console.error('Error fetching festas:', error);
            }
        };

        fetchFestas();
    }, []);



    return (
        <div className="border p-4 rounded bg-white bg-opacity-90 h-full" style={{ fontFamily: 'serif', color: '#4a2e2a' }}>
            <div ref={headerRef} className="sticky top-0 bg-white p-4 mb-4 rounded z-10 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-[#4a2e2a]">Lista de Festas</h2>
                <button 
                    onClick={() => setShowFilters(!showFilters)} 
                    className="text-[#4a2e2a] bg-[#f2e3c6] hover:text-[#f2e3c6] hover:bg-[#4a2e2a] rounded px-2 py-2 flex items-center transition-colors duration-300"
                >
                    {showFilters ? 'Hide Filters' : 'Show Filters'}
                </button>
            </div>
            {showFilters && (
                <div className="mb-6">
                    <form className="max-w-md mx-auto">
                        <label htmlFor="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                                <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                                </svg>
                            </div>
                            <input 
                                type="search" 
                                id="default-search" 
                                className=" block w-full p-4 pl-10 text-sm text-black rounded-lg bg-gray-100" 
                                placeholder="Search Festa..." 
                                required 
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </form>
                    <div className="mt-4">
                        <label className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Filter by Date</label>
                        <div className="flex items-center justify-center space-x-4 ">
                            <div className="pl-10 relative max-w-sm w-full ">
                                <DatePicker
                                    selected={startDate}
                                    onChange={date => setStartDate(date)}
                                    selectsStart
                                    startDate={startDate}
                                    endDate={endDate}
                                    placeholderText="Select start date"
                                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                                    todayButton="Today"
                                />
                                {startDate && (
                                    <button
                                        type="button"
                                        className="absolute flex items-center px-3 text-gray-500"
                                        onClick={() => setStartDate(null)}
                                    >
                                        <svg className="w-4 h-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M9.95 10l3.528 3.528a1 1 0 1 1-1.414 1.414L8.536 11.414l-3.529 3.53a1 1 0 1 1-1.415-1.415L7.12 10 3.586 6.472a1 1 0 0 1 1.415-1.414L9.95 8.586l3.529-3.53a1 1 0 0 1 1.415 1.415L11.378 10z" clipRule="evenodd"/>
                                        </svg>
                                    </button>
                                )}
                            </div>
                            <span className="text-gray-500">to</span>
                            <div className="pr-10 relative max-w-sm w-full">
                                <DatePicker
                                    selected={endDate}
                                    onChange={date => setEndDate(date)}
                                    selectsEnd
                                    startDate={startDate}
                                    endDate={endDate}
                                    minDate={startDate}
                                    placeholderText="Select end date"
                                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                                    todayButton="Today"
                                />
                                {endDate && (
                                    <button
                                        type="button"
                                        className="absolute flex items-center px-3 text-gray-500"
                                        onClick={() => setEndDate(null)}
                                    >
                                        <svg className="w-4 h-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M9.95 10l3.528 3.528a1 1 0 1 1-1.414 1.414L8.536 11.414l-3.529 3.53a1 1 0 1 1-1.415-1.415L7.12 10 3.586 6.472a1 1 0 0 1 1.415-1.414L9.95 8.586l3.529-3.53a1 1 0 0 1 1.415 1.415L11.378 10z" clipRule="evenodd"/>
                                        </svg>
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}
            <div className="grid grid-cols-1 gap-4" style={{ height: `${containerHeight}px`, overflowY: 'auto' }}>
                {festas.map((festa, index) => (
                    <Festa key={index} festa={festa} />
                ))}
            </div>
        </div>
    );
}

export default Festas;
