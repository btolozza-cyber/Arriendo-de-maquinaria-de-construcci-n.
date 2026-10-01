const contractsContainer =
    document.getElementById("contracts-container");


async function cargarContratos() {

    const token =
        localStorage.getItem("access_token");

    if (!token) {

        window.location.href = "/login/";

        return;
    }

    try {

        const response = await fetch(
            "/api/contratos/",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const contratos =
            await response.json();

        if (!response.ok) {

            throw new Error(
                "No fue posible cargar los contratos."
            );
        }

        renderizarContratos(contratos);

    } catch (error) {

        contractsContainer.innerHTML = `
            <div class="cart-empty">

                <h2>
                    Error al cargar los contratos
                </h2>

                <p>
                    ${error.message}
                </p>

            </div>
        `;

        console.error(error);
    }
}


function renderizarContratos(contratos) {

    if (contratos.length === 0) {

        contractsContainer.innerHTML = `
            <div class="cart-empty">

                <h2>
                    No tienes contratos
                </h2>

                <p>
                    Cuando confirmes un arriendo,
                    aparecerá aquí.
                </p>

                <a
                    href="/maquinaria/"
                    class="btn btn-primary"
                >
                    Explorar maquinaria
                </a>

            </div>
        `;

        return;
    }


    contractsContainer.innerHTML = "";


    contratos.forEach(contrato => {

        const card =
            document.createElement("article");

        card.className = "contract-card";


        let itemsHTML = "";


        contrato.items.forEach(item => {

            itemsHTML += `
                <div class="contract-item">

                    <div>
                        <span>
                            Maquinaria
                        </span>

                        <strong>
                            #${item.maquinaria}
                        </strong>
                    </div>

                    <div>
                        <span>
                            Inicio
                        </span>

                        <strong>
                            ${item.fecha_inicio}
                        </strong>
                    </div>

                    <div>
                        <span>
                            Término
                        </span>

                        <strong>
                            ${item.fecha_fin}
                        </strong>
                    </div>

                    <div>
                        <span>
                            Cantidad
                        </span>

                        <strong>
                            ${item.cantidad}
                        </strong>
                    </div>

                </div>
            `;
        });


        card.innerHTML = `

            <div class="contract-header">

                <div>

                    <p class="machinery-category">
                        CONTRATO
                    </p>

                    <h2>
                        Contrato #${contrato.id}
                    </h2>

                </div>

                <span class="contract-status">
                    ${contrato.estado}
                </span>

            </div>


            <div class="contract-date">

                Creado:
                ${new Date(
                    contrato.fecha_creacion
                ).toLocaleDateString("es-CL")}

            </div>


            <div class="contract-items">

                ${itemsHTML}

            </div>

        `;


        contractsContainer.appendChild(card);
    });
}


cargarContratos();