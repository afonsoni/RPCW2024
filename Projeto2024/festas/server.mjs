import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.get('/festas', async (req, res) => {
    const district = req.query.district || '';
    const county = req.query.county || '';

    const query = `
        PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?nome ?dataInicio ?dataFim ?desc ?regiao ?distrito ?concelho ?freguesia WHERE { 
            ?s rdf:type :Festa ;
               :nome ?nome ;
               :descricao ?desc ;
               :dataInicio ?dataInicio ;
               :dataFim ?dataFim ;
               :ocorreRegiao ?r ;
               :ocorreDistrito ?d .
            ?r :nome ?regiao .
            ?d :nome ?distrito .
            OPTIONAL { ?s :ocorreConcelho ?c . ?c :nome ?concelho . }
            OPTIONAL { ?s :ocorreFreguesia ?f . ?f :nome ?freguesia . }
            ${district ? `FILTER(?distrito = "${district}")` : ''}
            ${county ? `FILTER(?concelho = "${county}")` : ''}
        }
        ORDER BY (?dataInicio)
    `;

    try {
        const response = await fetch('http://localhost:7200/repositories/FestasRomarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-query',
                'Accept': 'application/sparql-results+json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        const formattedData = data.results.bindings.map(item => ({
            "Nome da Festa": item.nome.value,
            "Descrição": item.desc.value,
            "Data Inicio": item.dataInicio.value,
            "Data Fim": item.dataFim.value,
            "Distrito": item.distrito.value,
            "Região": item.regiao.value,
            "Concelho": item.concelho ? item.concelho.value : '',
            "Freguesia": item.freguesia ? item.freguesia.value : ''
        }));

        res.status(200).json(formattedData);
    } catch (error) {
        console.error('Error fetching data from GraphDB:', error);
        res.status(500).json({ error: 'Failed to fetch data' });
    }
});

app.get('/distritos', async (req, res) => {
    const query = `
    PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
    SELECT DISTINCT ?district WHERE {
        ?s a :Distrito;
            :nome ?district
    } ORDER BY ?district
    `;

    try {
        const response = await fetch('http://localhost:7200/repositories/FestasRomarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-query',
                'Accept': 'application/sparql-results+json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();

        const districts = data.results.bindings.map(b => b.district.value);
        res.status(200).json(districts);
    } catch (error) {
        console.error('Error fetching data from GraphDB:', error);
        res.status(500).json({ error: 'Failed to fetch data' });
    }
});


app.get('/concelhos', async (req, res) => {
    const { distrito} = req.query;

    const query = `
    PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
    SELECT DISTINCT ?concelho WHERE {
        ?s a :Distrito;
            :nome '${distrito}' ;
               :temConcelho ?c.
        ?c :nome ?concelho .
    } ORDER BY ?concelho
    `;

    try {
        const response = await fetch('http://localhost:7200/repositories/FestasRomarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-query',
                'Accept': 'application/sparql-results+json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();

        const concelhos = data.results.bindings.map(b => b.concelho.value);
        res.status(200).json(concelhos);
    } catch (error) {
        console.error('Error fetching data from GraphDB:', error);
        res.status(500).json({ error: 'Failed to fetch data' });
    }
});


app.get('/freguesias', async (req, res) => {
    const { concelho} = req.query;

    const query = `
    PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
        SELECT DISTINCT ?freguesia WHERE {
            ?s a :Concelho;
                :nome '${concelho}' ;
                   :temFreguesia ?freg.
            ?freg :nome ?freguesia .
            
        } ORDER BY ?freguesia
    `;

    try {
        const response = await fetch('http://localhost:7200/repositories/FestasRomarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-query',
                'Accept': 'application/sparql-results+json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();

        const freguesias = data.results.bindings.map(b => b.freguesia.value);
        res.status(200).json(freguesias);
    } catch (error) {
        console.error('Error fetching data from GraphDB:', error);
        res.status(500).json({ error: 'Failed to fetch data' });
    }
});

//http://localhost:5000/regiao?distrito=Vila%20Real
app.get('/regiao', async (req, res) => {
    const { distrito } = req.query;

    const query = `
        PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
        SELECT DISTINCT ?regiao WHERE {
            ?s rdf:type :Distrito ;
                :nome '${distrito}' ;
                :pertenceRegiao ?r .
            ?r :nome ?regiao .
        } ORDER BY ?regiao
    `;

    try {
        const response = await fetch('http://localhost:7200/repositories/FestasRomarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-query',
                'Accept': 'application/sparql-results+json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.results.bindings.length === 0) {
            throw new Error(`No region found for district: ${distrito}`);
        }

        const regiao = data.results.bindings[0].regiao.value;
        res.status(200).json({ regiao });
    } catch (error) {
        console.error('Error fetching region by district:', error);
        res.status(500).json({ error: 'Failed to fetch region by district' });
    }
});


app.get('/next_id', async (req, res) => {
    const query = `
        PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
        SELECT (COUNT(?s) AS ?n_festas) WHERE {
            ?s rdf:type :Festa .
        }
    `;

    try {
        const response = await fetch('http://localhost:7200/repositories/FestasRomarias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-query',
                'Accept': 'application/sparql-results+json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        const n_festas = parseInt(data.results.bindings[0].n_festas.value, 10);
        const next_id = n_festas + 1;

        res.status(200).json({ next_id });
    } catch (error) {
        console.error('Error fetching next ID:', error);
        res.status(500).json({ error: 'Failed to fetch next ID' });
    }
});


app.post('/criar_festa', async (req, res) => {
    try {
        let { nome, dataInicio, dataFim, distrito, concelho, freguesia, descricao } = req.body;

        // Obter o próximo ID disponível
        const idResponse = await fetch('http://localhost:5000/next_id');
        const idData = await idResponse.json();
        const id = idData.next_id;

        // Obter a região correspondente ao distrito
        const regiaoResponse = await fetch(`http://localhost:5000/regiao?distrito=${distrito}`);
        const regiaoData = await regiaoResponse.json();
        const regiao = regiaoData.regiao;

        console.log('Creating festa:', { id, nome, dataInicio, dataFim, distrito, concelho, freguesia, descricao, regiao });

        // passar data 14-06-2024 para 14/06/2024
        dataInicio = dataInicio.split('-').join('/');
        dataFim = dataFim.split('-').join('/');

        console.log(dataInicio);
        console.log(dataFim);

        // Construa sua consulta SPARQL para inserir os dados na ontologia
        const query = `
            PREFIX : <http://rpcw.di.uminho.pt/festas&romarias/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            INSERT DATA {
                :festa${id} rdf:type :Festa ;
                           :nome "${nome}" ;
                           :descricao "${descricao}" ;
                           :dataInicio "${dataInicio}" ;
                           :dataFim "${dataFim}" ;
                           :ocorreRegiao :regiao${id} ;
                           :ocorreDistrito :distrito${id} ;
                           :ocorreConcelho :concelho${id} ;
                           :ocorreFreguesia :freguesia${id} .

                :regiao${id} rdf:type :Regiao ;
                           :nome "${regiao}" .

                :distrito${id} rdf:type :Distrito ;
                           :nome "${distrito}" .

                :concelho${id} rdf:type :Concelho ;
                           :nome "${concelho}" .

                :freguesia${id} rdf:type :Freguesia ;
                           :nome "${freguesia}" .
            }
        `;

        const response = await fetch('http://localhost:7200/repositories/FestasRomarias/statements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/sparql-update',
                'Accept': 'application/json',
            },
            body: query
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        // Se a inserção for bem-sucedida, envie uma resposta de sucesso
        res.status(201).json({ message: 'Festa criada com sucesso!' });
    } catch (error) {
        console.error('Error creating festa:', error);
        res.status(500).json({ error: 'Failed to create festa' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
