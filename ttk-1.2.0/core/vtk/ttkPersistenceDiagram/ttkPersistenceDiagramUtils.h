#include <Debug.h>
#include <PersistenceDiagramUtils.h>

class vtkUnstructuredGrid;
class vtkDataArray;

/**
 * @brief Converts a Persistence Diagram in the VTK Unstructured Grid
 * format (as generated by the ttkPersistenceDiagram module) to the
 * ttk::DiagramType format.
 *
 * @param[out] diagram Vector to be filled with persistence pairs
 * @param[in] vtu Input VTK Unstructured Grid
 * @param[in] dbg Reference to a ttk::Debug instance (for error messages)
 *
 * @return 0 in case of success, negative number otherwise
 */
int VTUToDiagram(ttk::DiagramType &diagram,
                 vtkUnstructuredGrid *vtu,
                 const ttk::Debug &dbg);

/**
 * @brief Converts a Persistence Diagram in the
 * ttk::DiagramType format to the VTK Unstructured Grid
 * format (as generated by the ttkPersistenceDiagram module).
 *
 * @param[out] vtu Output VTK Unstructured Grid
 * @param[in] diagram Vector of persistence pairs
 * @param[in] inputScalars vtkDataArray pointer to input scalar field
 * @param[in] dbg Reference to a ttk::Debug instance (for error messages)
 * @param[in] dim Data-set dimensionality (to convert pair dimension to pair
 * type)
 * @param[in] embedInDomain Switch between the canonical and the embedded
 * representation
 *
 * @return 0 in case of success, negative number otherwise
 */
int DiagramToVTU(vtkUnstructuredGrid *vtu,
                 const ttk::DiagramType &diagram,
                 vtkDataArray *const inputScalars,
                 const ttk::Debug &dbg,
                 const int dim,
                 const bool embedInDomain);

/**
 * @brief Generate the spatial embedding of a given Persistence Diagram
 *
 * Use the pointData array `Coordinates` to project the Diagram
 *
 * @param[in] inputDiagram Input diagram in its canonical form
 * @param[out] outputDiagram Projected diagram inside the input domain
 * @param[in] dbg Debug instance (for logging and access to threadNumber_)
 *
 * @return 0 in case of success
 */
int ProjectDiagramInsideDomain(vtkUnstructuredGrid *const inputDiagram,
                               vtkUnstructuredGrid *const outputDiagram,
                               const ttk::Debug &dbg);

/**
 * @brief Generate the 2D embedding of a given Persistence Diagram
 *
 * Use the cellData arrays `Birth` and `Death` to project the Diagram
 *
 * @param[in] inputDiagram Input diagram in its spatial embedding form
 * @param[out] outputDiagram Projected diagram in its canonical form
 * @param[in] dbg Debug instance (for logging and access to threadNumber_)
 *
 * @return 0 in case of success
 */
int ProjectDiagramIn2D(vtkUnstructuredGrid *const inputDiagram,
                       vtkUnstructuredGrid *const outputDiagram,
                       const ttk::Debug &dbg);

/**
 * @brief Translate a diagram to a new position.
 *
 * @param[in,out] diagram Input diagram in its spatial embedding form
 * @param[in] trans Translation vector
 *
 * @return 0 in case of success
 */
int TranslateDiagram(vtkUnstructuredGrid *const diagram,
                     const std::array<double, 3> &trans);

/**
 * @brief Translate back a canonical diagram into its original position.
 *
 * Use the cellData array `Birth` as original coordinates
 *
 * @param[in,out] diagram Input diagram in its spatial embedding form
 * @param[in] dbg Debug instance (for logging and access to threadNumber_)
 *
 * @return 0 in case of success
 */
int ResetDiagramPosition(vtkUnstructuredGrid *const diagram,
                         const ttk::Debug &dbg);