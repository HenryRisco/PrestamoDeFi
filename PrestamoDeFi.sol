// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PrestamoDeFi {
    // VARIABLES DE ESTADO GLOBALES
    // Gestor del contrato inteligente
    address public socioPrincipal;

    // Esta estructura define un tipo de dato llamado Prestamo que tiene los siguientes campos
    // id: Identificador único del préstamo.
    // prestatario: Dirección del prestatario que solicita el préstamo.
    // monto: Monto del préstamo solicitado.
    // plazo: Plazo en el que el préstamo debe ser reembolsado.
    // tiempoSolicitud: Marca de tiempo en la que se realizó la solicitud del préstamo.
    // tiempoLimite: Marca de tiempo que indica el límite de tiempo para el reembolso.
    // aprobado: Indica si el préstamo ha sido aprobado.
    // reembolsado: Indica si el préstamo ha sido reembolsado.
    // liquidado: Indica si la garantía del préstamo ha sido liquidada.
    struct Prestamo {
        uint256 id;
        address prestatario;
        uint256 monto;
        uint256 plazo;
        uint256 tiempoSolicitud;
        uint256 tiempoLimite;
        bool aprobado;
        bool reembolsado;
        bool liquidado;
    }

    // Esta estructura define un tipo de dato llamado Cliente que tiene los siguientes campos
    // activado: Indica si el cliente está registrado y activo en el sistema.
    // saldoGarantia: Saldo total de garantías depositadas por el cliente.
    // prestamos: Mapeo de ID de préstamo a la estructura Prestamo.
    // prestamoIds: Lista de ID de préstamos asociados al cliente.
    struct Cliente {
        bool activado;
        uint256 saldoGarantia;
        mapping(uint256 => Prestamo) prestamos;
        uint256[] prestamoIds;
    }

    // Mapping clientes que relaciona el address del cliente con su struct Cliente
    mapping(address => Cliente) public clientes;

    // Mapping empleadosPrestamista que relaciona el address del empleado con su
    // valor booleano true/false en función de si se ha dado de alta como prestamista o no.
    mapping(address => bool) public empleadosPrestamista;
    
    // Eventos
    // SolicitudPrestamo: Se emite cuando un cliente solicita un préstamo.
    event SolicitudPrestamo(address indexed prestatario, uint256 monto, uint256 plazo);
    
    // PrestamoAprobado: Se emite cuando un prestamista aprueba un préstamo.
    event PrestamoAprobado(address indexed prestatario, uint256 monto);
    
    // PrestamoReembolsado: Se emite cuando un cliente reembolsa un préstamo.
    event PrestamoReembolsado(address indexed prestatario, uint256 monto);
    
    // GarantiaLiquidada: Se emite cuando un prestamista liquida la garantía de un préstamo.
    event GarantiaLiquidada(address indexed prestatario, uint256 monto);

    // SolicitudPrestamo
    //event SolicitudPrestamo(uint indexed id, address prestatario, uint monto, uint plazo, uint tiempoSolicitud);

    //  Modifiers
    // soloSocioPrincipal: Requiere que el remitente sea el socio principal del contrato.
    modifier soloSocioPrincipal() {
        require(socioPrincipal == msg.sender, "Error: no eres el propietario");
        // continue
        _;
    }

    // soloEmpleadoPrestamista: Requiere que el remitente sea un empleado con el rol de prestamista.
    modifier soloEmpleadoPrestamista() {
        require(empleadosPrestamista[msg.sender], "El remitente no es un empleado con el rol de prestamista");
        // continue
        _;
    } 


    // soloClienteRegistrado: Requiere que el sea un cliente registrado y activo.
    modifier soloClienteRegistrado() {
        require(clientes[msg.sender].activado, "El emisor no es un cliente activado");
        // continue
        _;
    }

    // Contructor
    // Asignaremos la variable socioPrincipal al emisor del despliegue del contrato.
    // Añadiremos socioPrincipal al mapping de empleadosPrestamista con valor true.
    constructor() {
        socioPrincipal = msg.sender;
        empleadosPrestamista[socioPrincipal] = true;
    }

    // La función pública altaPrestamista que se encargará de asignar al mapping de empleadosPrestamista el
    // nuevo address que se le pase como valor de entrada, siempre y cuando el prestamista no
    // esté dado previamente de alta.
    function altaPrestamista(address nuevoPrestamista) public soloSocioPrincipal {
        require(!empleadosPrestamista[nuevoPrestamista], "El prestamista ya esta dado de alta al sistema");
        empleadosPrestamista[nuevoPrestamista] = true;
    }

    // La función pública altaCliente que se encargará de asignar al mapping de clientes el nuevo address
    // que se le pase como valor de entrada, siempre y cuando el cliente no esté dado
    // previamente de alta
    function altaCliente(address nuevoCliente) public soloEmpleadoPrestamista {
        require(!clientes[nuevoCliente].activado, "El cliente ya esta dado de alta al sistema");
        
        Cliente storage structNuevoCliente = clientes[nuevoCliente];
        structNuevoCliente.saldoGarantia = 0;
        structNuevoCliente.activado = true;

    }

    // La función pública y payable se encargará de recibir ether del cliente para ser depositado
    // como garantía y actualizar la variable saldoGarantía del cliente.
    function depositarGarantia() public payable soloClienteRegistrado {
        clientes[msg.sender].saldoGarantia += msg.value;
    }

    // La función pública solicitarPréstamos permitirá al prestatario/cliente registrado solicitar un préstamo
    // seleccionando el monto y los plazos del mismo.
    function solicitarPrestamos(uint256 monto_, uint256 plazo_) public payable soloClienteRegistrado returns (uint) {
        require(clientes[msg.sender].saldoGarantia >= monto_, "El saldo de garantia no es suficiente para solicitar el prestamo");

        uint256 nuevoId = clientes[msg.sender].prestamoIds.length + 1;
        
        Cliente storage cliente = clientes[msg.sender];
        Prestamo storage nuevoPrestamo = cliente.prestamos[nuevoId];

        nuevoPrestamo.id = nuevoId;
        nuevoPrestamo.prestatario = msg.sender;
        nuevoPrestamo.monto = monto_;
        nuevoPrestamo.plazo = plazo_;
        nuevoPrestamo.tiempoSolicitud = block.timestamp;
        nuevoPrestamo.tiempoLimite = 0;
        nuevoPrestamo.aprobado = false;
        nuevoPrestamo.reembolsado = false;
        nuevoPrestamo.liquidado = false;

        cliente.prestamoIds.push(nuevoId);

        emit SolicitudPrestamo(msg.sender, monto_, plazo_);

        return nuevoId;
}

    // La función pública aprobarPrestamo permitirá al prestamista registrado aprobar un préstamo específico.
    function aprobarPrestamo(address prestatario_, uint256 id_) public soloEmpleadoPrestamista {
        Cliente storage prestatario = clientes[prestatario_];
        require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "El prestamo no existe para este prestatario");
        
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(!prestamo.aprobado, "El prestamo ya ha sido aprobado");
        require(!prestamo.reembolsado, "El prestamo ya ha sido reembolsado");
        require(!prestamo.liquidado, "El prestamo ya ha sido liquidado");
        
        prestamo.aprobado = true;
        prestamo.tiempoLimite = block.timestamp + prestamo.plazo;

        emit PrestamoAprobado(prestamo.prestatario, prestamo.monto);
    }

    // La función pública reembolsarPrestamo permitirá al prestatario registrado reembolsar la cantidad pertinente de un
    // préstamo específico.
    function reembolsarPrestamo(uint256 id_) public soloClienteRegistrado {
        Cliente storage prestatario = clientes[msg.sender];
        require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "El prestamo no existe para este prestatario");
         
        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(prestamo.prestatario == msg.sender, "Solo el prestatario puede reembolsar el prestamo");
        require(prestamo.aprobado, "El prestamo no est aaprobado");
        require(!prestamo.reembolsado, "El prestamo ya ha sido reembolsado");
        require(!prestamo.liquidado, "El prestamo ya ha sido liquidado");
        require(prestamo.tiempoLimite >= block.timestamp, "El plazo para reembolsar el prestamo ha vencido");
        
        // Transferir el monto del préstamo al socio principal
        payable(socioPrincipal).transfer(prestamo.monto);
        
        prestamo.reembolsado = true;
        prestatario.saldoGarantia -= prestamo.monto;

        emit PrestamoReembolsado(prestamo.prestatario, prestamo.monto);
    }

    // La función pública liquidarGarantia permitirá al prestamista registrado liquidar la cantidad pertinente de un
    // préstamo específico en base a la garantía depositada por el prestatario en caso de que el
    // tiempo límite habrá vencido. 
    function liquidarGarantia(address prestatario_, uint256 id_) public soloEmpleadoPrestamista {
        Cliente storage prestatario = clientes[prestatario_];
        require(id_ > 0 && id_ <= prestatario.prestamoIds.length, "El prestamo no existe para este prestatario");

        Prestamo storage prestamo = prestatario.prestamos[id_];
        require(prestamo.aprobado, "El prestamo no esta aprobado");
        require(!prestamo.reembolsado, "El prestamo ya ha sido reembolsado");
        require(!prestamo.liquidado, "El prestamo ya ha sido liquidado");
        require(prestamo.tiempoLimite < block.timestamp, "El tiempo limite del prestamo no ha vencido");
        
        // Transferir el monto de la garantía del prestatario al socio principal
        payable(socioPrincipal).transfer(prestatario.saldoGarantia);
        
        prestamo.liquidado = true;
        prestatario.saldoGarantia = 0;

        emit GarantiaLiquidada(prestatario_, prestamo.monto);
       
    }

    // La función pública obtenerPrestamosPorPrestatario permitirá obtener los identificadores de todos los préstamos solicitados
    // por el prestatario (recuerda establecer el tipo de mutabilidad correspondiente).
    function obtenerPrestamosPorPrestatario(address prestatario_) public view returns (uint256[] memory) {
        return clientes[prestatario_].prestamoIds;
    }

    // La función pública obtenerDetalleDePrestamo permitirá obtener todos los campos del struct Prestamo que queremos
    // consultar (recuerda establecer el tipo de mutabilidad correspondiente).
    function obtenerDetalleDePrestamo(address prestatario_, uint256 id_) public view returns (Prestamo memory) {
        return clientes[prestatario_].prestamos[id_];
    }

} 