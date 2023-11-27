import faiss
import numpy as np
import logging


def initialize_faiss_index(data_np):
    try:
        data_np = np.ascontiguousarray(data_np)  # Ensure C-contiguous layout
        dimension = data_np.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(data_np)
        return index
    except Exception as e:
        print(f"Error initializing FAISS index: {e}")
        return None

def convert_query(data_np, num_query):
    return data_np[num_query:num_query+1]

def search_similar_foods(query, index, k=20):
    try:
        logging.debug(f"Query data shape: {query.shape}")
        logging.debug(f"Query data type: {query.dtype}")

        D, I = index.search(query, k)

        logging.debug(f"Distances: {D}")
        logging.debug(f"Indices: {I}")

        return D, I
    except Exception as e:
        print(f"Error searching similar foods: {e}")
        return None, None


def convert_results(D, I, df, fields=['description', 'brandOwner', 'brandedFoodCategory', 
                                      'ingredients', 'Protein (g)', 'Total Lipid (g)', 
                                      'Carbohydrate (g)', 'Energy (kcal)']):
    try:
        # Check if all required fields are present in the dataframe
        missing_fields = [field for field in fields if field not in df.columns]
        if missing_fields:
            logging.error(f"Missing fields in dataframe while converting Search result: {missing_fields}")
            return None

        # Extracting relevant information using indices I from dataframe df
        results = df.iloc[I[0]][fields]
        results_list = results.to_dict(orient='records')

        # Adding the 'index' key to each dictionary in results_list
        for index, result in zip(I[0], results_list):
            result['index'] = int(index)

        response_data = {
            "distances": D.tolist(),
            "similar foods": results_list
        }

        # Log a concise message instead of the full data
        logging.debug(f"convert_results executed successfully. Number of results: {len(results_list)}")
        return response_data
    except Exception as e:
        logging.error(f"Error in convert_results: {e}")
        return None
