import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-cover bg-[#4a2e2a] text-white py-6 mt-auto"> {/* Adicionei padding extra para mais espaçamento */}
            <div className="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
                <div className="mb-4 md:mb-0 text-center md:text-left">
                    <span className="block text-sm sm:text-center">© 2023 Festas e Romarias. All Rights Reserved.</span>
                    <span className="block text-sm sm:text-center">Criado por Joana Pereira, Afonso Ferreira, and Fernando Alves.</span>
                </div>
                <div className="flex flex-col items-start md:items-center md:flex-row md:justify-between">
                    <div className="text-sm mr-6 text-center md:text-left">
                        <p className="mb-1">Telemóvel: 935842979</p>
                        <p>Email: <a href="mailto:pg53895@uminho.pt" className="hover:underline">pg53895@uminho.pt</a></p>
                    </div>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
