const maquinariaGrid =
    document.getElementById("maquinaria-grid");

const categoryFilter =
    document.getElementById("category-filter");


async function cargarMaquinarias(categoria = "") {

    const token =
        localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login/";
        return;
    }

    try {

        let url = "/api/maquinarias/";

        if (categoria) {
            url += `?categoria=${categoria}`;
        }

        const response = await fetch(
            url,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (response.status === 401) {

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            window.location.href = "/login/";
            return;
        }

        if (!response.ok) {

            throw new Error(
                `Error de API: ${response.status}`
            );
        }

        const data =
            await response.json();

        renderizarMaquinarias(data);

    } catch (error) {

        maquinariaGrid.innerHTML = `
            <p class="catalog-error">
                No fue posible cargar las maquinarias.
            </p>
        `;

        console.error(error);
    }
}


function renderizarMaquinarias(maquinarias) {

    maquinariaGrid.innerHTML = "";

    if (maquinarias.length === 0) {

        maquinariaGrid.innerHTML = `
            <div class="catalog-empty">

                <h3>
                    No hay maquinaria disponible
                </h3>

                <p>
                    No encontramos equipos para
                    la categoría seleccionada.
                </p>

            </div>
        `;

        return;
    }

    maquinarias.forEach(maquinaria => {

        const card =
            document.createElement("article");

        card.className =
            "machinery-card";

        card.innerHTML = `
            <div class="machinery-image">

                <span>
                    ${maquinaria.categoria}
                </span>

            </div>

            <div class="machinery-content">

                <p class="machinery-category">
                    ${maquinaria.categoria}
                </p>

                <h2>
                    ${maquinaria.nombre}
                </h2>

                <p class="machinery-description">
                    Equipo disponible para proyectos
                    de construcción.
                </p>

                <div class="machinery-details">

                    <div>

                        <span>
                            Tarifa diaria
                        </span>

                        <strong>
                            $${Number(
                                maquinaria.tarifa_diaria
                            ).toLocaleString("es-CL")}
                        </strong>

                    </div>

                    <div>

                        <span>
                            Garantía
                        </span>

                        <strong>
                            $${Number(
                                maquinaria.garantia
                            ).toLocaleString("es-CL")}
                        </strong>

                    </div>

                </div>

                <button
                    class="btn btn-primary machinery-button"
                    data-id="${maquinaria.id}"
                    data-nombre="${maquinaria.nombre}"
                >
                    Arrendar
                </button>

            </div>
        `;

        maquinariaGrid.appendChild(card);
    });
}


categoryFilter.addEventListener(
    "change",
    () => {

        cargarMaquinarias(
            categoryFilter.value
        );

    }
);


maquinariaGrid.addEventListener(
    "click",
    (event) => {

        const button =
            event.target.closest(
                ".machinery-button"
            );

        if (!button) {
            return;
        }

        const maquinariaId =
            button.dataset.id;

        const maquinariaNombre =
            button.dataset.nombre;

        mostrarFormularioArriendo(
            maquinariaId,
            maquinariaNombre
        );
    }
);


function mostrarFormularioArriendo(
    maquinariaId,
    maquinariaNombre
) {

    const formulario =
        document.createElement("div");

    formulario.className =
        "rental-form";

    formulario.innerHTML = `
        <div class="rental-form-content">

            <h2>
                Arrendar ${maquinariaNombre}
            </h2>

            <div class="form-group">

                <label for="fecha-inicio">
                    Fecha de inicio
                </label>

                <input
                    type="date"
                    id="fecha-inicio"
                    required
                >

            </div>

            <div class="form-group">

                <label for="fecha-fin">
                    Fecha de término
                </label>

                <input
                    type="date"
                    id="fecha-fin"
                    required
                >

            </div>

            <div class="form-group">

                <label for="cantidad">
                    Cantidad
                </label>

                <input
                    type="number"
                    id="cantidad"
                    min="1"
                    value="1"
                    required
                >

            </div>

            <div class="rental-form-actions">

                <button
                    type="button"
                    class="btn btn-primary"
                    id="confirmar-arriendo"
                >
                    Agregar al carro
                </button>

                <button
                    type="button"
                    class="btn btn-secondary"
                    id="cancelar-arriendo"
                >
                    Cancelar
                </button>

            </div>

            <p
                id="rental-error"
                class="login-error"
            ></p>

        </div>
    `;

    document.body.appendChild(formulario);


    document
        .getElementById("cancelar-arriendo")
        .addEventListener(
            "click",
            () => {

                formulario.remove();

            }
        );


    document
        .getElementById("confirmar-arriendo")
        .addEventListener(
            "click",
            () => {

                agregarAlCarro(
                    maquinariaId,
                    formulario
                );

            }
        );
}


async function agregarAlCarro(
    maquinariaId,
    formulario
) {

    const fechaInicio =
        document.getElementById(
            "fecha-inicio"
        ).value;

    const fechaFin =
        document.getElementById(
            "fecha-fin"
        ).value;

    const cantidad =
        Number(
            document.getElementById(
                "cantidad"
            ).value
        );

    const errorElement =
        document.getElementById(
            "rental-error"
        );

    errorElement.textContent = "";


    if (!fechaInicio || !fechaFin) {

        errorElement.textContent =
            "Debes seleccionar ambas fechas.";

        return;
    }


    if (fechaInicio >= fechaFin) {

        errorElement.textContent =
            "La fecha de inicio debe ser anterior a la fecha de término.";

        return;
    }


    if (cantidad <= 0) {

        errorElement.textContent =
            "La cantidad debe ser mayor que cero.";

        return;
    }


    const token =
        localStorage.getItem(
            "access_token"
        );


    if (!token) {

        window.location.href =
            "/login/";

        return;
    }


    try {

        const response = await fetch(
            "/api/items-carro/",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    maquinaria: maquinariaId,
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    cantidad: cantidad
                })
            }
        );


        const data =
            await response.json();


        if (response.status === 401) {

            localStorage.removeItem(
                "access_token"
            );

            localStorage.removeItem(
                "refresh_token"
            );

            window.location.href =
                "/login/";

            return;
        }


        if (!response.ok) {

            throw new Error(
                data.detail ||
                data.non_field_errors?.[0] ||
                "No fue posible agregar la maquinaria al carro."
            );
        }


        formulario.remove();

        alert(
            "La maquinaria fue agregada al carro."
        );


    } catch (error) {

        errorElement.textContent =
            error.message;

        console.error(error);
    }
}


cargarMaquinarias();