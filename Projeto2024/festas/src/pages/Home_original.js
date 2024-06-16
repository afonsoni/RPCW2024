import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Header from '../components/Header';
import Descricao from '../components/Descricao';
import Festas from '../components/Festas';
import Mapa from '../components/Mapa';
import Criar from '../pages/Criar';
import Footer from '../components/Footer';

export default function Home() {
    const location = useLocation();
    const [showScrollButton, setShowScrollButton] = useState(false);
    const [festas, setFestas] = useState([]);


    useEffect(() => {
        if (location.state && location.state.scrollTo) {
            const section = document.getElementById(location.state.scrollTo);
            if (section) {
                const headerOffset = 70;
                const elementPosition = section.getBoundingClientRect().top + window.pageYOffset;
                const offsetPosition = elementPosition - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth',
                });
            }
        }

        const handleScroll = () => {
            if (window.scrollY > 100) {
                setShowScrollButton(true);
            } else {
                setShowScrollButton(false);
            }
        };

        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, [location]);

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth',
        });
    };

    return (
        <div className="bg-cover bg-center min-h-screen" style={{ backgroundColor: '#f2e3c6' }}>
            <Header />
            <main className="flex-grow flex flex-col mt-20">
                <div className="bg-white p-4 w-full"> <Descricao /> </div>
                <div id="festas-section" className=" p-4 w-full bg-brown-800" style={{ marginTop: '20px', paddingTop: '20px' }}>
                    <div className="flex justify-center flex-nowrap my-8 px-32">
                        <div className="md:w-1/2 p-4"> <Festas /> </div>
                        <div className="md:w-1/2 p-4"> <Mapa /> </div>
                    </div>
                </div>  
            </main>
            <Footer />
            {showScrollButton && (
                <button 
                    className="fixed bottom-10 right-10 bg-[#4a2e2a] text-white p-4 rounded-full shadow-lg"
                    onClick={scrollToTop}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                    </svg>
                </button>
            )}
        </div>
    );
}
