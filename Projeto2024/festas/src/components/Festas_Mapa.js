import React, { useState, useEffect, useRef, forwardRef } from 'react';
import Festa from './Festa'; 
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { ReactComponent as PortugalMap } from '../assets/mapa/portugal_map.svg'; 
import { ReactComponent as AveiroSvg } from '../assets/mapa/aveiro.svg';
import { ReactComponent as BejaSvg } from '../assets/mapa/beja.svg';
import { ReactComponent as BragaSvg } from '../assets/mapa/braga.svg';
import { ReactComponent as BragancaSvg } from '../assets/mapa/braganca.svg';
import { ReactComponent as CasteloBrancoSvg } from '../assets/mapa/castelo_branco.svg';
import { ReactComponent as CoimbraSvg } from '../assets/mapa/coimbra.svg';
import { ReactComponent as EvoraSvg } from '../assets/mapa/evora.svg';
import { ReactComponent as FaroSvg } from '../assets/mapa/faro.svg';
import { ReactComponent as GuardaSvg } from '../assets/mapa/guarda.svg';
import { ReactComponent as LeiriaSvg } from '../assets/mapa/leiria.svg';
import { ReactComponent as LisbonSvg } from '../assets/mapa/lisboa.svg';
import { ReactComponent as PortalegreSvg } from '../assets/mapa/portalegre.svg';
import { ReactComponent as PortoSvg } from '../assets/mapa/porto.svg';
import { ReactComponent as SantaremSvg } from '../assets/mapa/santarem.svg';
import { ReactComponent as SetubalSvg } from '../assets/mapa/setubal.svg';
import { ReactComponent as VianaDoCasteloSvg } from '../assets/mapa/viana_do_castelo.svg';
import { ReactComponent as VilaRealSvg } from '../assets/mapa/vila_real.svg';
import { ReactComponent as ViseuSvg } from '../assets/mapa/viseu.svg';
import './Mapa.css';
import '../App.css';

const Festas_Mapa = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [showFilters, setShowFilters] = useState(false);
    const [containerHeight, setContainerHeight] = useState(0);
    const [festas, setFestas] = useState([]);
    const [hoveredName, setHoveredName] = useState('');
    const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCounty, setSelectedCounty] = useState(null);
    const headerRef = useRef(null);
    const [selectedCounties, setSelectedCounties] = useState([]);

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
                let response;
                if (selectedDistrict != null) {
                    if (selectedCounty != null) {
                        response = await fetch(`http://localhost:5000/festas?district=${selectedDistrict}&county=${selectedCounty}`);
                    } else {
                        response = await fetch(`http://localhost:5000/festas?district=${selectedDistrict}`);
                    }
                } else {
                    response = await fetch('http://localhost:5000/festas');
                }

                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                const data = await response.json();

                data.sort((a, b) => {
                    const [dayA, monthA, yearA] = a['Data Inicio'].split("-");
                    const [dayB, monthB, yearB] = b['Data Inicio'].split("-");
                    return new Date(yearA, monthA - 1, dayA) - new Date(yearB, monthB - 1, dayB);
                });

                setFestas(data);
            } catch (error) {
                console.error('Error fetching festas:', error);
            }
        };

        fetchFestas();
    }, [selectedDistrict, selectedCounty]);

    const convertDate = str => {
        const [day, month, year] = str.split("/");
        return new Date(`${year}-${month}-${day}`);
    }

    const currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0);

    const filteredFestas = festas
    .filter(festa =>
        festa["Nome da Festa"].toLowerCase().includes(searchTerm.toLowerCase()) &&
        (convertDate(festa['Data Fim']) >= (startDate || currentDate)) &&
        (!endDate || convertDate(festa['Data Inicio']) <= endDate)
    )
    .sort((a, b) => convertDate(a['Data Inicio']) - convertDate(b['Data Inicio']));

    const CustomInput = forwardRef(({ value, onClick }, ref) => (
        <button
            type="button"
            className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-16 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a]"
            onClick={onClick}
            ref={ref}
        >
            {value || 'dd-mm-yyyy'}
        </button>
    ));

    const decodeURIComponent = (str) => {
        return str.replace(/\\x([0-9A-Fa-f]{2})/g, (match, p1) => {
            return String.fromCharCode('0x' + p1);
        });
    }

    const handleMouseEnter = (event) => {
        if (event.target.tagName === 'path') {
            let nameEncoded = event.target.getAttribute('class');
            let name = decodeURIComponent(nameEncoded);
            console.log(name);
            setHoveredName(name);
        }
    };

    const handleMouseLeave = () => {
        setHoveredName('');
    };

    const handleMouseMove = (event) => {
        setTooltipPosition({
            x: event.clientX + 10,
            y: event.clientY + 10
        });
        setHoveredName('');
    };

    const handleClick = (event) => {
        if (event.target.tagName === 'path') {
            if (!selectedDistrict) {
                let districtEncoded = event.target.getAttribute('class');
                let district = decodeURIComponent(districtEncoded);
                console.log(district);
                console.log(district);
                setSelectedDistrict(district);
            } else {
                let countyEncoded = event.target.getAttribute('class');
                let county = decodeURIComponent(countyEncoded);
                
                setSelectedCounties((prevSelectedCounties) => {
                    if (prevSelectedCounties.includes(county)) {
                        // Remove o concelho da lista
                        return prevSelectedCounties.filter(item => item !== county);
                    } else {
                        // Adiciona o concelho à lista
                        return [...prevSelectedCounties, county];
                    }
                });
                
                setSelectedCounty(county);
            }
        }
    };
    
    
    const close = () => {
        setSelectedDistrict(null);
        setSelectedCounty(null);
    }

    const generateDistrict = (district, SvgComponent) => {
        const highlightedSvg = React.cloneElement(<SvgComponent />, {
            className: (countyClass) => selectedCounties.includes(countyClass) ? 'selected-county' : ''
        });
    
        return (
            <div className="flex flex-col items-center justify-center w-full h-full">
                <h2 className="text-2xl font-bold mb-4 px-4">{district}</h2>
                {selectedCounty}
                <div className="district-svg-container">
                    <div className="district-svg-container">
                    {highlightedSvg}
                </div>
                </div>
            </div>
        );
    };

    const districtMap = {
        Aveiro: generateDistrict('Aveiro', AveiroSvg),
        Beja: generateDistrict('Beja', BejaSvg),
        Braga: generateDistrict('Braga', BragaSvg),
        Bragança: generateDistrict('Bragança', BragancaSvg),
        'Castelo Branco': generateDistrict('Castelo Branco', CasteloBrancoSvg),
        Coimbra: generateDistrict('Coimbra', CoimbraSvg),
        Évora: generateDistrict('Évora', EvoraSvg),
        Faro: generateDistrict('Faro', FaroSvg),
        Guarda: generateDistrict('Guarda', GuardaSvg),
        Leiria: generateDistrict('Leiria', LeiriaSvg),
        Lisboa: generateDistrict('Lisboa', LisbonSvg),
        Portalegre: generateDistrict('Portalegre', PortalegreSvg),
        Porto: generateDistrict('Porto', PortoSvg),
        Santarém: generateDistrict('Santarém', SantaremSvg),
        Setúbal: generateDistrict('Setúbal', SetubalSvg),
        'Viana do Castelo': generateDistrict('Viana do Castelo', VianaDoCasteloSvg),
        'Vila Real': generateDistrict('Vila Real', VilaRealSvg),
        Viseu: generateDistrict('Viseu', ViseuSvg)
    };

    return (
        <div className="flex justify-center flex-nowrap my-8 px-32">
            <div className="md:w-1/2 p-4"> 
                <div className="border p-4 rounded bg-white bg-opacity-90 h-full" style={{ fontFamily: 'serif', color: '#4a2e2a' }}>
                    <div ref={headerRef} className="sticky top-0 bg-white p-4 mb-4 rounded z-10 flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-[#4a2e2a]">Lista de Festas</h2>
                        <button 
                            onClick={() => setShowFilters(!showFilters)} 
                            className="text-[#4a2e2a] bg-[#f2e3c6] hover:text-[#f2e2c6] hover:bg-[#4a2e2a] rounded px-2 py-2 flex items-center transition-colors duration-300"                        >
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
                                        className="block w-full p-4 pl-10 text-sm text-black rounded-lg bg-gray-100" 
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
                                            dateFormat="dd-MM-yyyy"
                                            selectsStart
                                            startDate={startDate}
                                            endDate={endDate}
                                            customInput={<CustomInput />}
                                            isClearable
                                            placeholderText="Select start date"
                                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                                            todayButton="Today"
                                        />

                                    </div>
                                    <span className="text-gray-500">to</span>
                                    <div className="pr-10 relative max-w-sm w-full">
                                        <DatePicker
                                            selected={endDate}
                                            onChange={date => setEndDate(date)}
                                            dateFormat="dd-MM-yyyy"
                                            selectsEnd
                                            startDate={startDate}
                                            endDate={endDate}
                                            minDate={startDate}
                                            customInput={<CustomInput />}
                                            isClearable
                                            placeholderText="Select end date"
                                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                                            todayButton="Today"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div className="flex flex-col gap-4" style={{ height: `${containerHeight}px`, overflowY: 'auto' }}>                        {filteredFestas.map((festa, index) => (
                            <Festa key={index} festa={festa} />
                        ))}
                    </div>
                </div>
            </div>
            <div className="md:w-1/2 p-4 relative">
    <div className="border p-4 rounded bg-white bg-opacity-90 h-full" style={{ fontFamily: 'serif', color: '#4a2e2a' }}>
        <div ref={headerRef} className="sticky top-0 bg-white p-4 mb-4 rounded z-10 flex justify-between items-center">
            <h2 className="text-2xl font-bold text-[#4a2e2a] px-4">Mapa de Festas</h2>
            <button 
                className="bg-[#f2e3c6] text-[#4a2e2a] hover:bg-[#4a2e2a] hover:text-[#f2e3c6] rounded px-4 py-2 transition-colors duration-300"
                onClick={close}
            >
                Fechar
            </button>
        </div>
        <div 
            onClick={handleClick}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onMouseMove={handleMouseMove}
            className="flex flex-col items-center justify-center w-auto h-auto max-h-[80vh] p-4"
        >
            {selectedDistrict ? (
                <div className="flex flex-col items-center justify-center w-full h-auto">
                    {districtMap[selectedDistrict]}
                </div>
            ) : (
                <PortugalMap className="w-full h-auto max-h-[70vh] object-contain p-4"/>
            )}
        </div>
        {hoveredName && (
            <div 
                className="tooltip absolute text-white bg-black rounded px-2 py-1"
                style={{
                    left: `${tooltipPosition.x}px`,
                    top: `${tooltipPosition.y}px`
                }}
            >
                {hoveredName}
            </div>
        )}
    </div>
</div>


        </div>
    );
}

export default Festas_Mapa;
