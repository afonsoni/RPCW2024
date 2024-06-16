import React, { useState, forwardRef } from 'react';
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

    const handleStartDateChange = (date) => {
        setStartDate(date);
    };

    const handleEndDateChange = (date) => {
        setEndDate(date);
    };

    const handleCreateEvent = async () => {
        try {
            const response = await fetch('http://localhost:5000/criar_festa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },

                body: JSON.stringify({
                    nome: eventName,
                    dataInicio: startDate.toLocaleDateString('pt-PT'),
                    dataFim: endDate.toLocaleDateString('pt-PT'),
                    distrito: district,
                    concelho: county,
                    freguesia: parish,
                    descricao: description
                })

            });

            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }

            const data = await response.json();
            console.log(data); // Exibe a resposta do servidor (opcional)

            // Lógica para lidar com o sucesso da criação da festa (opcional)
        } catch (error) {
            console.error('Error creating event:', error);
            // Lógica para lidar com o erro (opcional)
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
                <h2 className="text-2xl font-bold mb-8 mt-8 px-4 text-right text-[#4a2e2a]">Criar Evento</h2>

                <form className="w-full max-w-lg">
                    <div className="mb-6">
                        <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-name">
                            Nome do Evento
                        </label>
                        <input className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a]" id="grid-name" type="text" placeholder="Nome do Evento" value={eventName} onChange={(e) => setEventName(e.target.value)} />
                    </div>
                    <div className="flex flex-wrap -mx-3 mb-6">
                        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-start-date">
                                Data de Início
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
                            />
                        </div>
                        <div className="w-full md:w-1/2 px-3">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-end-date">
                                Data de Fim
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
                            />
                        </div>
                    </div>
                    <div className="flex flex-wrap -mx-3 mb-6">
                        <div className="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-district">
                                Distrito
                            </label>
                            <input className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a]" id="grid-district" type="text" placeholder="Distrito" value={district} onChange={(e) => setDistrict(e.target.value)} />
                        </div>
                        <div className="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-county">
                                Concelho
                            </label>
                            <input className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a]" id="grid-county" type="text" placeholder="Concelho" value={county} onChange={(e) => setCounty(e.target.value)} />
                        </div>
                        <div className="w-full md:w-1/3 px-3 mb-6 md:mb-0">
                            <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-parish">
                                Freguesia
                            </label>
                            <input className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a]" id="grid-parish" type="text" placeholder="Freguesia" value={parish} onChange={(e) => setParish(e.target.value)} />
                        </div>
                    </div>
                    <div className="mb-6">
                        <label className="block uppercase tracking-wide text-[#4a2e2a] text-xs font-bold mb-2" htmlFor="grid-description">
                            Descrição
                        </label>
                        <textarea className="appearance-none block w-full bg-[#f2e3c6] text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-[#4a2e2a]" id="grid-description" placeholder="Descrição do Evento" value={description} onChange={(e) => setDescription(e.target.value)} />
                    </div>
                    <button className="bg-[#4a2e2a] hover:bg-[#635346] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" onClick={handleCreateEvent}>
                        Criar Evento
                    </button>
                </form>
            </main>
            <Footer className="mt-auto" />
        </div>
    );
}

