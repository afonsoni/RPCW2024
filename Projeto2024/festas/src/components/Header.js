import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const scrollToSection = (sectionId) => {
    const section = document.getElementById(sectionId);
    const headerOffset = 40;
    const elementPosition = section.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - headerOffset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth',
    });
  };

  const handleHomeClick = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    navigate('/');
  };

  const handleCriarClick = () => {
    window.scrollTo({ top: 0 });
    navigate('/CriarFesta');
  };

  const handleFestasClick = () => {
    if (location.pathname === '/') {
      scrollToSection('festas-section');
    } else {
      navigate('/', { state: { scrollTo: 'festas-section' } });
    }
  };

  return (
    <header className="fixed top-0 left-0 right-0 p-4 z-50" style={{ backgroundColor: '#f2e3c6' }}>
      <div className="flex items-center justify-between mr-32 ml-32"> {/* Remover container mx-auto */}
        <div className="flex items-center">
          <img src={logo} alt="Logo" className="h-20 ml-2" /> {/* Logo à esquerda com margem reduzida */}
        </div>
        <link href="https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap" rel="stylesheet"></link>
        <h1 className="text-4xl font-bold absolute left-1/2 transform -translate-x-1/2" style={{ fontFamily: 'MedievalSharp', color: '#4a2e2a' }}>Festas e Romarias</h1> {/* Título centralizado */}
        <div className="flex items-center space-x-2 mr-2"> {/* Botões à direita com margem reduzida */}
          <button
            onClick={handleHomeClick}
            className="bg-white text-[#4a2e2a] rounded px-4 py-2 transition-colors duration-300 hover:bg-[#4a2e2a] hover:text-white"
          >
            Home
          </button>
          <button
            onClick={handleFestasClick}
            className="bg-white text-[#4a2e2a] rounded px-4 py-2 transition-colors duration-300 hover:bg-[#4a2e2a] hover:text-white"
          >
            Festas
          </button>
          <button
            onClick={handleCriarClick}
            className="bg-white text-[#4a2e2a] rounded px-4 py-2 transition-colors duration-300 hover:bg-[#4a2e2a] hover:text-white"
          >
            Criar Festa
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
