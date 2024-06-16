import React, { useState, useEffect, forwardRef } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { registerLocale } from 'react-datepicker';
import pt from 'date-fns/locale/pt';

registerLocale('pt', pt);

export default function Criar() {
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [eventName, setEventName] = useState('');
    const [district, setDistrict] = useState('');
    const [county, setCounty] = useState('');
    const [parish, setParish] = useState('');
    const [description, setDescription] = useState('');
    const [districts, setDistricts] = useState([]);
    const [counties, setCounties] = useState([]);
    const [parishes, setParishes] = useState([]);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:5000/distritos');
                const data = await response.json();
                setDistricts(data);
            } catch (error) {
                console.error('Error fetching districts:', error);
            }
        };
    
        fetchData();
    }, []);
    

    useEffect(() => {
        const fetchData = async () => {
            if (district) {
                try {
                    const response = await fetch(`http://localhost:5000/concelhos?distrito=${district}`);
                    const data = await response.json();
                    setCounties(data);
                } catch (error) {
                    console.error('Error fetching counties:', error);
                }
            } else {
                setCounties([]);
                setCounty('');
            }
        };
    
        fetchData();
    }, [district]);
    

    useEffect(() => {
        const fetchData = async () => {
            if (county) {
                try {
                    const response = await fetch(`http://localhost:5000/freguesias?concelho=${county}`);
                    const data = await response.json();
                    setParishes(data);
                } catch (error) {
                    console.error('Error fetching parishes:', error);
                }
            } else {
                setParishes([]);
                setParish('');
            }
        };
    
        fetchData();
    }, [county]);
    

    const handleStartDateChange = (date) => {
        setStartDate(date);
    };

    const handleEndDateChange = (date) => {
        setEndDate(date);
    };

    const handleCreateEvent = async () => {
        console.log("Handle Create Event Called");

        if (!eventName || !startDate || !endDate || !district || !county) {
            alert('Por favor, preencha todos os campos obrigatórios.');
            return;
        }   

        console.log(eventName, startDate, endDate, district, county, parish, description)

        try {
            const response = await fetch('http://localhost:5000/criar_festa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nome: eventName,
                    dataInicio: startDate.toISOString().split('T')[0].split('-').reverse().join('-'),
                    dataFim: endDate.toISOString().split('T')[0].split('-').reverse().join('-'),
                    distrito: district,
                    concelho: county,
                    freguesia: parish,
                    descricao: description
                })
            });

            console.log("Resposta da criação:", response); // Log da resposta

            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }

            const data = await response.json();
            // Atualizar a mensagem de sucesso
            setSuccessMessage('Festa criada com sucesso!');

            // Limpar os campos
            setEventName('');
            setStartDate(null);
            setEndDate(null);
            setDistrict('');
            setCounty('');
            setParish('');
            setDescription('');
            // Remover a mensagem de sucesso após 5 segundos
            setTimeout(() => setSuccessMessage(''), 5000);
            setErrorMessage('');

            // Lógica para lidar com o sucesso da criação da festa (opcional)
        } catch (error) {
            console.error('Error creating event:', error);
            // Lógica para lidar com o erro (opcional)
            setErrorMessage('Erro ao criar festa. Por favor, tente novamente.');
            setSuccessMessage('');
        }
    };

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

    return (
        <div className="flex flex-col bg-cover bg-center bg-white min-h-screen">
            <Header />
            <main className="flex-grow flex flex-col items-center justify-center mt-28 md:mt-0" id="criar-section">
                <h2 className="text-3xl font-bold mb-8 mt-8 px-4 text-right text-[#4a2e2a]">Criar Festa</h2>
                
                {successMessage && (
                <div className="mb-4 text-green-500 text-xl">
                    {successMessage}
                </div>
                )}
                
                {errorMessage && (
                <div className="mb-4 text-red-500 text-xl">
                    {errorMessage}
                </div>
                )}

                <form className="w-full max-w-2xl">
                    <div className="mb-6">
                        <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-name">
                            Nome da Festa <span className="text-red-500">*</span>
                        </label>
                        <input 
                            className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a] text-xl" 
                            id="grid-name" 
                            type="text" 
                            placeholder="Nome da Festa" 
                            value={eventName} 
                            onChange={(e) => setEventName(e.target.value)} 
                            required 
                        />
                    </div>
                    <div className="flex flex-wrap -mx-3 mb-6">
                        <div className="w-full md:w-5/12 px-3 ">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-start-date">
                                Data de Início <span className="text-red-500">*</span>
                            </label>
                            <DatePicker
                                selected={startDate}
                                onChange={handleStartDateChange}
                                dateFormat="dd-MM-yyyy"
                                placeholderText="dd-mm-yyyy"
                                customInput={<CustomInput />}
                                locale="pt"
                                isClearable
                                todayButton="Hoje"
                                required
                            />
                        </div>
                        <div className="w-full md:w-5/12 px-3">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-end-date">
                                Data de Fim <span className="text-red-500">*</span>
                            </label>
                            <DatePicker
                                selected={endDate}
                                onChange={handleEndDateChange}
                                dateFormat="dd-MM-yyyy"
                                placeholderText="dd-mm-yyyy"
                                customInput={<CustomInput />}
                                locale="pt"
                                isClearable
                                todayButton="Hoje"
                                required
                            />
                        </div>
                    </div>
                    <div className="flex flex-wrap -mx-3 mb-6">
                        <div className="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-district">
                                Distrito <span className="text-red-500">*</span>
                            </label>
                            <select
                                className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a] text-xl"
                                id="grid-district"
                                value={district}
                                onChange={(e) => setDistrict(e.target.value)}
                                required
                            >
                                <option value="">Selecione um distrito</option>
                                {districts.map((dist) => (
                                    <option key={dist} value={dist}>
                                        {dist}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-county">
                                Concelho <span className="text-red-500">*</span>
                            </label>
                            <select
                                className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a] text-xl"
                                id="grid-county"
                                value={county}
                                onChange={(e) => setCounty(e.target.value)}
                                disabled={!district}
                                required
                            >
                                <option value="">Selecione um concelho</option>
                                {counties.map((cnt) => (
                                    <option key={cnt} value={cnt}>
                                        {cnt}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-parish">
                                Freguesia
                            </label>
                            <select
                                className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a] text-xl"
                                id="grid-parish"
                                value={parish}
                                onChange={(e) => setParish(e.target.value)}
                                disabled={!county}
                            >
                                <option value="">Selecione uma freguesia</option>
                                {parishes.map((par) => (
                                    <option key={par} value={par}>
                                        {par}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="mb-6">
                        <label className="block uppercase tracking-wide text-[#4a2e2a] text-xl font-bold mb-2" htmlFor="grid-description">
                            Descrição
                        </label>
                        <textarea className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a] text-xl" id="grid-description" placeholder="Descrição da Festa" value={description} onChange={(e) => setDescription(e.target.value)} />
                    </div>
                    <button className="bg-[#4a2e2a] hover:bg-[#635346] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline text-2xl" type="button" onClick={handleCreateEvent}>
                        Criar Evento
                    </button>
                </form>
            </main>
            <Footer className="mt-auto" />
        </div>
    );
}
