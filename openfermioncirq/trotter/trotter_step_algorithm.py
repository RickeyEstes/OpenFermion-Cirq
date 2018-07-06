#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import Optional, Sequence, Tuple

import cirq
from cirq import abc
from openfermion import DiagonalCoulombHamiltonian


class TrotterStepAlgorithm(metaclass=abc.ABCMeta):
    """A method for performing a Trotter step.

    This class assumes that Hamiltonian evolution using a Trotter-Suzuki product
    formula is performed in the following steps:
        1. Perform some preparatory operations (for instance, a basis change).
        2. Perform a number of Trotter steps. Each Trotter step may induce a
           permutation on the ordering in which qubits represent fermionic
           modes.
        3. Perform some finishing operations.

    Attributes:
        controlled: A bool indicating whether the Trotter step is controlled
            by a control qubit.
    """

    controlled = False

    def prepare(self,
                qubits: Sequence[cirq.QubitId],
                hamiltonian: DiagonalCoulombHamiltonian,
                control_qubit: Optional[cirq.QubitId]=None
                ) -> cirq.OP_TREE:
        """Operations to perform before doing the Trotter steps.

        Args:
            qubits: The qubits on which to perform operations. They should
                be sorted so that the j-th qubit in the Sequence holds the
                occupation of the j-th fermionic mode.
            hamiltonian: The Hamiltonian to simulate.
            control_qubit: The control qubit, if the algorithm is controlled.
        """
        # Default: do nothing
        return ()

    @abc.abstractmethod
    def trotter_step(
            self,
            qubits: Sequence[cirq.QubitId],
            hamiltonian: DiagonalCoulombHamiltonian,
            time: float,
            control_qubit: Optional[cirq.QubitId]=None
            ) -> cirq.OP_TREE:
        """Yield operations to perform a Trotter step.

        Args:
            qubits: The qubits on which to apply the Trotter step.
            hamiltonian: The Hamiltonian to simulate.
            time: The evolution time.
            control_qubit: The control qubit, if the algorithm is controlled.
        """
        pass

    def step_qubit_permutation(self,
                               qubits: Sequence[cirq.QubitId],
                               control_qubit: Optional[cirq.QubitId]=None
                               ) -> Tuple[Sequence[cirq.QubitId],
                                          Optional[cirq.QubitId]]:
        """The qubit permutation induced by a single Trotter step.

        Returns:
            A tuple whose first element is the new list of system qubits and
            second element is the new control qubit
        """
        # Default: identity permutation
        return qubits, control_qubit

    def finish(self,
               qubits: Sequence[cirq.QubitId],
               hamiltonian: DiagonalCoulombHamiltonian,
               n_steps: int,
               control_qubit: Optional[cirq.QubitId]=None,
               omit_final_swaps: bool=False
               ) -> cirq.OP_TREE:
        """Operations to perform after all Trotter steps are done.

        Args:
            qubits: The qubits on which to perform operations.
            hamiltonian: The Hamiltonian to simulate.
            n_steps: The total number of Trotter steps that have been performed.
            control_qubit: The control qubit, if the algorithm is controlled.
            omit_final_swaps: Whether or not to omit swap gates at the end of
                the circuit.
        """
        # Default: do nothing
        return ()
