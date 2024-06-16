import React from 'react';
import imagemDescricao from '../assets/fotos_juntas.png';

const Descricao = () => {
  const description = "Bem-vindo às Festas e Romarias de Portugal. Descubra as mais belas e tradicionais festas e romarias de Portugal. Viaje no tempo e conheça as celebrações que mantêm viva a nossa cultura e história.";

  return (
    <div className="flex justify-center my-8 px-4">
      <div className="max-w-6xl flex flex-col md:flex-row items-center">
        <div className="w-full md:w-1/2 p-4">
          <img src={imagemDescricao} alt="Descrição Imagem" className="w-full h-auto" />
        </div>
        <div className="w-full md:w-1/2 md:ml-8 mt-4 md:mt-0 p-4 bg-white rounded-lg shadow-lg">
          <h1 className="text-3xl md:text-5xl font-bold mb-6 md:mb-10" style={{ fontFamily: 'MedievalSharp', color: '#4a2e2a' }}>Conceito deste site e sua importância</h1>
          <p className="text-lg md:text-2xl" style={{ fontFamily: 'Lora', color: '#4a2e2a' }}>{description}</p>
        </div>
      </div>
    </div>
  );
};

export default Descricao;
