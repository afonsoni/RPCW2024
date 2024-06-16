import React, { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa';

const Festa = ({ festa }) => {

    const [showMore, setShowMore] = useState(false);

    const location = [festa["Freguesia"], festa["Concelho"], festa["Distrito"]]
        .filter(Boolean)
        .join(", "); 

    return (
        <div className="border p-4 mb-4 rounded shadow-md bg-white">
            <h2 className="text-2xl font-semibold">{festa["Nome da Festa"]}</h2>
            <p className = " text-xl " >
                {festa["Data Inicio"]}
                {festa["Data Inicio"] != festa["Data Fim"] && ` - ${festa["Data Fim"]}`}
            </p>            
            {location && <p className = " text-xl ">{location} </p>}
            {showMore && <p className="mt-2 text-xl">{festa["Descrição"]}</p>}
            {festa["Descrição"] != "None" && festa["Descrição"] != "" && (
                <button
                    className="mt-2 text-xl  text-[#4a2e2a] hover:text-[#f2e3c6] hover:bg-[#4a2e2a] rounded px-1 py-1 transition-colors duration-300 flex items-center"
                    onClick={() => setShowMore(!showMore)}
                >
                    {showMore ? <FaChevronUp /> : <FaChevronDown />}
                    <span className="ml-1">{showMore ? 'Mostrar menos' : 'Mostrar mais'}</span>
                </button>
            )}
        </div>
    );
};


export default Festa;
