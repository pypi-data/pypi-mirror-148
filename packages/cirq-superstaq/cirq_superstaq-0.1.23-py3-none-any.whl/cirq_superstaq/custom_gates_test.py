import itertools
import textwrap

import cirq
import numpy as np
import packaging
import pytest
import sympy

import cirq_superstaq


def test_zz_swap_gate() -> None:
    theta = 0.123
    gate = cirq_superstaq.ZZSwapGate(theta)

    assert str(gate) == "ZZSwapGate(0.123)"
    assert repr(gate) == "cirq_superstaq.ZZSwapGate(0.123)"
    cirq.testing.assert_equivalent_repr(gate, setup_code="import cirq_superstaq")

    expected = np.array(
        [[1, 0, 0, 0], [0, 0, np.exp(1j * theta), 0], [0, np.exp(1j * theta), 0, 0], [0, 0, 0, 1]]
    )
    assert np.allclose(cirq.unitary(gate), expected)

    qubits = cirq.LineQubit.range(3)
    operation = gate(qubits[0], qubits[2])
    assert cirq.decompose_once(operation) == [
        cirq.CX(qubits[0], qubits[2]),
        cirq.CX(qubits[2], qubits[0]),
        cirq.rz(theta).on(qubits[2]),
        cirq.CX(qubits[0], qubits[2]),
    ]

    cirq.testing.assert_has_consistent_apply_unitary(gate)
    cirq.testing.assert_decompose_is_consistent_with_unitary(gate, ignoring_global_phase=True)
    cirq.testing.assert_consistent_resolve_parameters(gate)
    cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(gate)

    assert gate**1 == gate
    assert gate**0 == cirq_superstaq.ZZSwapGate(0.0)
    assert gate**-1 == cirq_superstaq.ZZSwapGate(-0.123)

    with pytest.raises(TypeError, match="unsupported operand type"):
        _ = gate**1.23


def test_zz_swap_circuit() -> None:
    qubits = cirq.LineQubit.range(3)
    operation = cirq_superstaq.ZZSwapGate(0.456 * np.pi)(qubits[0], qubits[2])
    circuit = cirq.Circuit(operation)

    expected_diagram = textwrap.dedent(
        """
        0: ───ZZSwap(0.456π)───
              │
        2: ───ZZSwap(0.456π)───
        """
    )

    expected_qasm = textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0, 1, 2]
        qreg q[3];


        zzswap(pi*0.456) q[0],q[2];
        """
    )

    cirq.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.to_qasm(header="", qubit_order=qubits) == expected_qasm

    circuit = cirq.Circuit(cirq_superstaq.ZZSwapGate(0.0)(qubits[0], qubits[1]))
    assert circuit.to_qasm() == cirq.Circuit(cirq.SWAP(qubits[0], qubits[1])).to_qasm()


def test_zz_swap_parameterized() -> None:
    gate = cirq_superstaq.ZZSwapGate(sympy.var("θ"))
    cirq.testing.assert_consistent_resolve_parameters(gate)

    with pytest.raises(TypeError, match="cirq.unitary failed. Value doesn't have"):
        _ = cirq.unitary(gate)

    with pytest.raises(TypeError, match="No Pauli expansion"):
        _ = cirq.pauli_expansion(gate)


def test_zx_matrix() -> None:
    np.testing.assert_allclose(
        cirq.unitary(cirq_superstaq.ZX),
        np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, -1, 0]]),
    )


def test_zx_str() -> None:
    assert str(cirq_superstaq.ZX) == "ZX"
    assert str(cirq_superstaq.ZX**0.5) == "ZX**0.5"
    assert str(cirq_superstaq.ZXPowGate(global_shift=0.1)) == "ZX"

    iZZ = cirq_superstaq.ZXPowGate(global_shift=0.5)
    assert str(iZZ) == "ZX"


def test_zx_repr() -> None:
    assert repr(cirq_superstaq.ZXPowGate()) == "cirq_superstaq.ZX"
    assert repr(cirq_superstaq.ZXPowGate(exponent=0.5)) == "(cirq_superstaq.ZX**0.5)"
    assert (
        repr(cirq_superstaq.ZXPowGate(exponent=0.5, global_shift=0.123))
        == "cirq_superstaq.ZXPowGate(exponent=0.5, global_shift=0.123)"
    )

    cirq.testing.assert_equivalent_repr(
        cirq_superstaq.ZXPowGate(), setup_code="import cirq_superstaq"
    )


def test_zx_circuit() -> None:
    a, b = cirq.LineQubit.range(2)

    op = cirq_superstaq.CR(a, b)

    cirq.testing.assert_has_diagram(
        cirq.Circuit(op),
        textwrap.dedent(
            """
            0: ───Z───
                  │
            1: ───X───
            """
        ),
    )

    assert cirq.Circuit(op, op**0.25).to_qasm(header="") == textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0, 1]
        qreg q[2];


        rzx(pi*1.0) q[0],q[1];
        rzx(pi*0.25) q[0],q[1];
        """
    )


def test_acecr_init() -> None:
    cirq_superstaq.AceCR("+-")
    cirq_superstaq.AceCR("-+", np.pi / 3)
    with pytest.raises(ValueError, match="Polarity must be"):
        cirq_superstaq.AceCR("++")


def test_acecr_circuit_diagram_info() -> None:
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq_superstaq.AceCRMinusPlus(*qubits))
    assert str(circuit) == textwrap.dedent(
        """\
        0: ───AceCR-+(Z side)───
              │
        1: ───AceCR-+(X side)───"""
    )

    circuit = cirq.Circuit(cirq_superstaq.AceCRPlusMinus(*reversed(qubits)))
    assert str(circuit) == textwrap.dedent(
        """\
        0: ───AceCR+-(X side)───
              │
        1: ───AceCR+-(Z side)───"""
    )

    circuit = cirq.Circuit(cirq_superstaq.AceCR("+-", np.pi)(*qubits))
    assert str(circuit) == textwrap.dedent(
        """\
        0: ───AceCR+-(Z side)──────────
              │
        1: ───AceCR+-(X side)|Rx(π)|───"""
    )


def test_acecr_qasm() -> None:
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq_superstaq.AceCR("+-").on(*qubits),
        cirq_superstaq.AceCR("-+").on(*reversed(qubits)),
        cirq_superstaq.AceCR("-+", np.pi / 2).on(*qubits),
    )

    assert circuit.to_qasm(header="") == textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0, 1]
        qreg q[2];


        acecr_pm q[0],q[1];
        acecr_mp q[1],q[0];
        acecr_mp_rx(pi*0.5) q[0],q[1];
        """
    )


def test_acecr_eq() -> None:
    assert cirq_superstaq.AceCRPlusMinus == cirq_superstaq.AceCR("+-")
    assert cirq_superstaq.AceCRPlusMinus != cirq_superstaq.AceCR("-+")
    assert cirq_superstaq.AceCR("+-", np.pi) == cirq_superstaq.AceCR("+-", np.pi)
    assert cirq_superstaq.AceCR("-+", np.pi) != cirq_superstaq.AceCR("+-", np.pi)

    assert cirq_superstaq.AceCR("+-", np.pi) == cirq_superstaq.AceCR("+-", 5 * np.pi)
    assert cirq_superstaq.AceCR("+-", np.pi) == cirq_superstaq.AceCR("+-", 3 * np.pi)

    assert cirq.approx_eq(cirq_superstaq.AceCR("+-", np.pi), cirq_superstaq.AceCR("+-", -np.pi))
    assert cirq.approx_eq(cirq_superstaq.AceCR("+-", np.pi), cirq_superstaq.AceCR("+-", 3 * np.pi))


def test_acecr_repr_and_str() -> None:
    assert repr(cirq_superstaq.AceCRMinusPlus) == "cirq_superstaq.AceCR('-+')"
    assert (
        repr(cirq_superstaq.AceCR("+-", np.pi)) == "cirq_superstaq.AceCR('+-', 3.141592653589793)"
    )
    cirq.testing.assert_equivalent_repr(
        cirq_superstaq.AceCRMinusPlus, setup_code="import cirq_superstaq"
    )
    cirq.testing.assert_equivalent_repr(
        cirq_superstaq.AceCR("+-", np.pi), setup_code="import cirq; import cirq_superstaq"
    )
    assert str(cirq_superstaq.AceCRMinusPlus) == "AceCR-+"
    assert str(cirq_superstaq.AceCR("+-", np.pi)) == "AceCR+-|Rx(π)|"


def test_acecr_decompose() -> None:
    a = cirq.LineQubit(0)
    b = cirq.LineQubit(1)
    circuit = cirq.Circuit(cirq.decompose_once(cirq_superstaq.AceCRMinusPlus(a, b)))
    assert len(circuit) == 3 and len(list(circuit.all_operations())) == 3

    circuit = cirq.Circuit(cirq.decompose_once(cirq_superstaq.AceCR("+-", -np.pi / 2)(a, b)))
    assert len(circuit) == 3 and len(list(circuit.all_operations())) == 4


def test_barrier() -> None:
    n = 3
    gate = cirq_superstaq.Barrier(n)

    assert str(gate) == "Barrier(3)"
    assert repr(gate) == "cirq_superstaq.Barrier(3)"

    cirq.testing.assert_equivalent_repr(gate, setup_code="import cirq_superstaq")

    operation = gate.on(*cirq.LineQubit.range(3))
    assert cirq.decompose(operation) == [operation]

    circuit = cirq.Circuit(operation)
    expected_qasm = textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0, 1, 2]
        qreg q[3];


        barrier q[0],q[1],q[2];
        """
    )
    assert circuit.to_qasm(header="") == expected_qasm

    cirq.testing.assert_has_diagram(
        circuit,
        textwrap.dedent(
            """
            0: ───│───
                  │
            1: ───│───
                  │
            2: ───│───
            """
        ),
        use_unicode_characters=True,
    )

    cirq.testing.assert_has_diagram(
        circuit,
        textwrap.dedent(
            """
            0: ---|---
                  |
            1: ---|---
                  |
            2: ---|---
            """
        ),
        use_unicode_characters=False,
    )

    # make sure optimizations don't drop Barriers:
    cirq.DropNegligible()(circuit)
    assert circuit == cirq.Circuit(operation)
    assert cirq.trace_distance_bound(gate) == 1.0


def test_parallel_gates() -> None:
    gate = cirq_superstaq.ParallelGates(cirq.CZ, cirq.CZ**0.5, cirq.CZ**-0.5)
    qubits = cirq.LineQubit.range(6)
    operation = gate(*qubits)
    circuit = cirq.Circuit(operation)

    expected_diagram = textwrap.dedent(
        """
        0: ───@₁────────
              │
        1: ───@₁────────
              │
        2: ───@₂────────
              │
        3: ───@₂^0.5────
              │
        4: ───@₃────────
              │
        5: ───@₃^-0.5───
        """
    )
    cirq.testing.assert_has_diagram(circuit, expected_diagram)
    cirq.testing.assert_equivalent_repr(gate, setup_code="import cirq, cirq_superstaq")
    assert repr(gate) == "cirq_superstaq.ParallelGates(cirq.CZ, (cirq.CZ**0.5), (cirq.CZ**-0.5))"
    assert str(gate) == "ParallelGates(CZ, CZ**0.5, CZ**-0.5)"

    assert cirq.decompose(operation) == [
        cirq.CZ(qubits[0], qubits[1]),
        cirq.CZ(qubits[2], qubits[3]) ** 0.5,
        cirq.CZ(qubits[4], qubits[5]) ** -0.5,
    ]
    cirq.testing.assert_decompose_is_consistent_with_unitary(gate, ignoring_global_phase=True)

    assert gate**0.5 == cirq_superstaq.ParallelGates(
        cirq.CZ**0.5, cirq.CZ**0.25, cirq.CZ**-0.25
    )

    with pytest.raises(ValueError, match="ParallelGates cannot contain measurements"):
        _ = cirq_superstaq.ParallelGates(cirq.X, cirq.MeasurementGate(1, key="1"))


def test_parallel_gates_equivalence_groups() -> None:
    qubits = cirq.LineQubit.range(4)
    gate = cirq_superstaq.ParallelGates(cirq.X, cirq_superstaq.ZX, cirq.Y)
    operation = gate(*qubits[:4])
    assert [gate.qubit_index_to_equivalence_group_key(i) for i in range(4)] == [0, 1, 2, 3]
    for permuted_qubits in itertools.permutations(operation.qubits):
        if permuted_qubits == operation.qubits:
            assert operation == gate(*permuted_qubits)
        else:
            assert operation != gate(*permuted_qubits)

    gate = cirq_superstaq.ParallelGates(cirq.X, cirq.X, cirq_superstaq.ZZSwapGate(1.23))
    operation = gate(*qubits)
    assert [gate.qubit_index_to_equivalence_group_key(i) for i in range(4)] == [0, 0, 2, 2]

    equivalent_targets = [
        (qubits[0], qubits[1], qubits[2], qubits[3]),
        (qubits[1], qubits[0], qubits[2], qubits[3]),
        (qubits[0], qubits[1], qubits[3], qubits[2]),
        (qubits[1], qubits[0], qubits[3], qubits[2]),
    ]
    for permuted_qubits in itertools.permutations(operation.qubits):
        if permuted_qubits in equivalent_targets:
            assert operation == gate(*permuted_qubits)
        else:
            assert operation != gate(*permuted_qubits)

    with pytest.raises(ValueError, match="index out of range"):
        _ = gate.qubit_index_to_equivalence_group_key(4)

    with pytest.raises(ValueError, match="index out of range"):
        _ = gate.qubit_index_to_equivalence_group_key(-1)


@pytest.mark.skipif(
    packaging.version.parse("0.14.0.dev20220126174724")
    < packaging.version.parse(cirq.__version__)
    < packaging.version.parse("0.15.0.dev20220420201205"),
    reason="https://github.com/quantumlib/Cirq/issues/5148",
)
def test_parallel_gates_equivalence_groups_nonadjacent() -> None:  # pragma: no cover
    """Fails in cirq version 0.14.x due to https://github.com/quantumlib/Cirq/issues/5148"""
    qubits = cirq.LineQubit.range(4)
    gate = cirq_superstaq.ParallelGates(cirq.X, cirq_superstaq.ZZSwapGate(1.23), cirq.X)
    assert [gate.qubit_index_to_equivalence_group_key(i) for i in range(4)] == [0, 1, 1, 0]

    operation = gate(*qubits)
    equivalent_targets = [
        (qubits[0], qubits[1], qubits[2], qubits[3]),
        (qubits[0], qubits[2], qubits[1], qubits[3]),
        (qubits[3], qubits[1], qubits[2], qubits[0]),
        (qubits[3], qubits[2], qubits[1], qubits[0]),
    ]
    for permuted_qubits in itertools.permutations(operation.qubits):
        if permuted_qubits in equivalent_targets:
            assert operation == gate(*permuted_qubits)
        else:
            assert operation != gate(*permuted_qubits)


def test_rgate() -> None:
    qubit = cirq.LineQubit(0)

    rot_gate = cirq_superstaq.RGate(4.56 * np.pi, 1.23 * np.pi)
    cirq.testing.assert_equivalent_repr(rot_gate, setup_code="import cirq_superstaq")
    assert str(rot_gate) == f"RGate({rot_gate.exponent}π, {rot_gate.phase_exponent}π)"
    assert rot_gate**-1 == cirq_superstaq.RGate(-rot_gate.theta, rot_gate.phi)

    circuit = cirq.Circuit(rot_gate.on(qubit))

    # build RGate decomposition manually
    decomposed_circuit = cirq.Circuit(
        cirq.rz(-rot_gate.phi).on(qubit),
        cirq.rx(rot_gate.theta).on(qubit),
        cirq.rz(+rot_gate.phi).on(qubit),
    )

    assert np.allclose(cirq.unitary(circuit), cirq.unitary(decomposed_circuit))

    expected_qasm = textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0]
        qreg q[1];


        r(pi*4.56,pi*-0.77) q[0];
        """
    )
    assert circuit.to_qasm(header="") == expected_qasm

    circuit = cirq.Circuit(cirq_superstaq.RGate(np.pi, 0.5 * np.pi).on(qubit))
    cirq.testing.assert_has_diagram(circuit, "0: ───RGate(π, 0.5π)───")


def test_parallel_rgate() -> None:
    qubits = cirq.LineQubit.range(2)

    rot_gate = cirq_superstaq.ParallelRGate(1.23 * np.pi, 4.56 * np.pi, len(qubits))
    cirq.testing.assert_equivalent_repr(rot_gate, setup_code="import cirq; import cirq_superstaq")
    text = f"RGate({rot_gate.phase_exponent}π, {rot_gate.exponent}π) x {len(qubits)}"
    assert str(rot_gate) == text
    assert rot_gate**-1 == cirq_superstaq.ParallelRGate(
        -rot_gate.theta, rot_gate.phi, len(qubits)
    )

    circuit = cirq.Circuit(rot_gate.on(*qubits))

    # build ParallelRGate decomposition manually
    manual_circuit = cirq.Circuit(
        [cirq_superstaq.RGate(rot_gate.theta, rot_gate.phi).on(qubit) for qubit in qubits]
    )

    assert np.allclose(cirq.unitary(circuit), cirq.unitary(manual_circuit))

    expected_qasm = textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0, 1]
        qreg q[2];


        GR(pi*1.23,pi*0.56) q[0],q[1];
        """
    )
    assert circuit.to_qasm(header="") == expected_qasm

    circuit = cirq.Circuit(
        cirq_superstaq.ParallelRGate(np.pi, 0.5 * np.pi, len(qubits)).on(*qubits)
    )
    expected_diagram = textwrap.dedent(
        """
        0: ───RGate(π, 0.5π)───
              │
        1: ───#2───────────────
        """
    )

    expected_qasm = textwrap.dedent(
        """\
        OPENQASM 2.0;
        include "qelib1.inc";


        // Qubits: [0, 1]
        qreg q[2];


        GR(pi*1.0,pi*0.5) q[0],q[1];
        """
    )

    cirq.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.to_qasm(header="", qubit_order=qubits) == expected_qasm


def test_iitoffoli() -> None:
    qubits = cirq.LineQubit.range(3)

    gate = cirq_superstaq.AQTITOFFOLI

    assert np.allclose(
        cirq.unitary(gate(*qubits)),
        # yapf: disable
        np.array(
            [
                [0, 1j, 0, 0, 0, 0, 0, 0],
                [1j, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
            ]
        ),
        # yapf: enable
    )


def test_custom_resolver() -> None:
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    circuit += cirq_superstaq.ZZSwapGate(1.23).on(qubits[0], qubits[1])
    circuit += cirq_superstaq.AceCRPlusMinus(qubits[0], qubits[1])
    circuit += cirq_superstaq.Barrier(2).on(qubits[0], qubits[1])
    circuit += cirq_superstaq.CR(qubits[0], qubits[1])
    circuit += cirq_superstaq.AceCRMinusPlus(qubits[0], qubits[1])
    circuit += cirq_superstaq.AceCR("+-", -np.pi / 2)(qubits[0], qubits[1])
    circuit += cirq_superstaq.ParallelGates(cirq.X, cirq_superstaq.ZX).on(
        qubits[0], qubits[2], qubits[3]
    )
    circuit += cirq_superstaq.custom_gates.MSGate(rads=0.5).on(qubits[0], qubits[1])
    circuit += cirq_superstaq.RGate(1.23, 4.56).on(qubits[0])
    circuit += cirq_superstaq.ParallelRGate(1.23, 4.56, len(qubits)).on(*qubits)
    circuit += cirq_superstaq.AQTITOFFOLI(qubits[0], qubits[1], qubits[2])
    circuit += cirq.CX(qubits[0], qubits[1])

    json_text = cirq.to_json(circuit)
    resolvers = [cirq_superstaq.custom_gates.custom_resolver, *cirq.DEFAULT_RESOLVERS]
    assert cirq.read_json(json_text=json_text, resolvers=resolvers) == circuit
