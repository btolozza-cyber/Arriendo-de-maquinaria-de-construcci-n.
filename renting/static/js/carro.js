const cartContainer = document.getElementById("cart-container");


async function cargarCarro() {

    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/login/";
        return;
    }

    try {

        const response = await fetch(
            "/api/items-carro/",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("No fue posible cargar el carro.");
        }

        const items = await response.json();

        renderizarCarro(items);

    } catch (error) {

        cartContainer.innerHTML = `
            <div class="cart-empty">
                <h2>Error al cargar el carro</h2>
                <p>${error.message}</p>
            </div>
        `;

        console.error(error);
    }
}


function renderizarCarro(items) {

    if (!items.length) {

        cartContainer.innerHTML = `
            <div class="cart-empty">

                <h2>Tu carro está vacío</h2>

                <p>
                    Agrega maquinaria desde nuestro catálogo.
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

    let total = 0;

    cartContainer.innerHTML = `
        <div class="cart-list"></div>

        <div class="cart-summary">

            <span>Total del arriendo</span>

            <strong id="cart-total">$0</strong>

            <button
                id="checkout-button"
                class="btn btn-primary"
            >
                Confirmar contrato
            </button>

        </div>
    `;

    const cartList =
        document.querySelector(".cart-list");

    items.forEach(item => {

        total += Number(item.costo_arriendo);

        const card = document.createElement("article");

        card.className = "cart-item";

        card.innerHTML = `
            <div class="cart-item-main">

                <div>

                    <p class="machinery-category">
                        MAQUINARIA
                    </p>

                    <h2>
                        ${item.maquinaria_nombre}
                    </h2>

                </div>

                <div class="cart-item-actions">

                    <button
                        class="cart-edit"
                        data-id="${item.id}"
                    >
                        Editar
                    </button>

                    <button
                        class="cart-delete"
                        data-id="${item.id}"
                    >
                        Eliminar
                    </button>

                </div>

            </div>

            <div class="cart-item-details">

                <div>
                    <span>Inicio</span>
                    <strong>${item.fecha_inicio}</strong>
                </div>

                <div>
                    <span>Término</span>
                    <strong>${item.fecha_fin}</strong>
                </div>

                <div>
                    <span>Cantidad</span>
                    <strong>${item.cantidad}</strong>
                </div>

                <div>
                    <span>Costo</span>
                    <strong>
                        $${Number(
                            item.costo_arriendo
                        ).toLocaleString("es-CL")}
                    </strong>
                </div>

            </div>
        `;

        cartList.appendChild(card);
    });

    document.getElementById("cart-total").textContent =
        `$${total.toLocaleString("es-CL")}`;


    document
        .querySelectorAll(".cart-edit")
        .forEach(button => {

            button.addEventListener("click", () => {

                const item = items.find(
                    item => item.id == button.dataset.id
                );

                mostrarEditarItem(item);

            });

        });


    document
        .querySelectorAll(".cart-delete")
        .forEach(button => {

            button.addEventListener("click", () => {

                eliminarItem(button.dataset.id);

            });

        });


    document
        .getElementById("checkout-button")
        .addEventListener(
            "click",
            confirmarContrato
        );
}


function mostrarEditarItem(item) {

    cartContainer.innerHTML = `

        <div class="edit-cart">

            <p class="section-tag">
                EDITAR ARRIENDO
            </p>

            <h2>
                Modificar maquinaria
            </h2>

            <div class="form-group">

                <label for="edit-fecha-inicio">
                    Fecha de inicio
                </label>

                <input
                    type="date"
                    id="edit-fecha-inicio"
                    value="${item.fecha_inicio}"
                >

            </div>

            <div class="form-group">

                <label for="edit-fecha-fin">
                    Fecha de término
                </label>

                <input
                    type="date"
                    id="edit-fecha-fin"
                    value="${item.fecha_fin}"
                >

            </div>

            <div class="form-group">

                <label for="edit-cantidad">
                    Cantidad
                </label>

                <input
                    type="number"
                    id="edit-cantidad"
                    min="1"
                    value="${item.cantidad}"
                >

            </div>

            <div class="edit-actions">

                <button
                    id="save-edit"
                    class="btn btn-primary"
                >
                    Guardar cambios
                </button>

                <button
                    id="cancel-edit"
                    class="btn btn-secondary"
                >
                    Cancelar
                </button>

            </div>

            <p
                id="edit-error"
                class="login-error"
            ></p>

        </div>
    `;


    document
        .getElementById("cancel-edit")
        .addEventListener(
            "click",
            cargarCarro
        );


    document
        .getElementById("save-edit")
        .addEventListener(
            "click",
            () => actualizarItem(item.id)
        );
}


async function actualizarItem(itemId) {

    const token =
        localStorage.getItem("access_token");

    const fechaInicio =
        document.getElementById(
            "edit-fecha-inicio"
        ).value;

    const fechaFin =
        document.getElementById(
            "edit-fecha-fin"
        ).value;

    const cantidad =
        Number(
            document.getElementById(
                "edit-cantidad"
            ).value
        );

    const errorElement =
        document.getElementById("edit-error");


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


    try {

        const response = await fetch(
            `/api/items-carro/${itemId}/`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    cantidad: cantidad
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.non_field_errors?.[0] ||
                data.detail ||
                "No fue posible actualizar el arriendo."
            );
        }


        await cargarCarro();

    } catch (error) {

        errorElement.textContent =
            error.message;

        console.error(error);
    }
}


async function eliminarItem(itemId) {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `/api/items-carro/${itemId}/`,
        {
            method: "DELETE",

            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {

        alert(
            "No fue posible eliminar el item."
        );

        return;
    }

    await cargarCarro();
}


async function confirmarContrato() {

    const token =
        localStorage.getItem("access_token");

    try {

        const carrosResponse = await fetch(
            "/api/carros/",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const carros = await carrosResponse.json();

        if (!carros.length) {

            throw new Error(
                "No se encontró tu carro."
            );
        }

        const carro = carros[0];

        const response = await fetch(
            `/api/carros/${carro.id}/checkout/`,
            {
                method: "POST",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "No fue posible confirmar el contrato."
            );
        }

        alert(
            `Contrato #${data.id} creado correctamente.`
        );

        await cargarCarro();

    } catch (error) {

        console.error(error);

        alert(error.message);
    }
}


cargarCarro();