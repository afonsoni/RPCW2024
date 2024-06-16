import React, { useState } from 'react';
import { ReactComponent as PortugalMap } from '../assets/mapa/portugal_map.svg'; // Importar arquivo SVG do mapa de Portugal
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

const Mapa = () => {
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCounty, setSelectedCounty] = useState(null);

    const decodeURIComponent = (str) => {
        return str.replace(/\\x([0-9A-Fa-f]{2})/g, (match, p1) => {
            return String.fromCharCode('0x' + p1);
        });
    }

    const handleClick = (event) => {
        if (event.target.tagName === 'path') {
            if (!selectedDistrict) {
                let districtEncoded = event.target.getAttribute('class');
                let district = decodeURIComponent(districtEncoded);
                setSelectedDistrict(district);
                console.log(district);
            } else {
                if (!event.target.classList.contains("selected")) {
                    let countyEncoded = event.target.getAttribute('class');
                    let county = decodeURIComponent(countyEncoded);
                    console.log(county);
                } else {
                    setSelectedCounty(null);
                }
            }
        }
    };

    const close = () => {
        setSelectedDistrict(null);
    }

    const generateDistrict = (district, SvgComponent) => {
        return (
            <div>
                <h2 className="text-2xl font-bold mb-4 px-4">{district}</h2>
                {selectedCounty}
                <SvgComponent />
            </div>
        );
    }

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
        <div className="border p-4 rounded bg-white bg-opacity-90 h-full overflow-y-auto" style={{ fontFamily: 'serif', color: '#4a2e2a' }}>
            <h2 className="text-2xl font-bold mb-4 px-4">Mapa de Festas</h2>
            <div onClick={handleClick}>
                {selectedDistrict ? (
                    <div className="text-center width:300px height:300px">
                        {districtMap[selectedDistrict]}
                        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={close}>Fechar
                        </button>
                    </div>
                ) : (
                    <PortugalMap />
                )}
            </div>
            
        </div>
    );
}

export default Mapa;
