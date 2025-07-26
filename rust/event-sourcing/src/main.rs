use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

struct Transaction {
    id: usize,
    amount: f32,
}

impl Transaction {
    fn new(id: usize, amount: f32) -> Self {
        Transaction { id, amount }
    }
}

fn main() {
    let (tx, rx) = std::sync::mpsc::channel();
    let counter = Arc::new(AtomicUsize::new(1));

    let tx1 = tx.clone();
    let counter1 = Arc::clone(&counter);
    fn send_transactions(
        tx: std::sync::mpsc::Sender<Transaction>,
        counter: Arc<AtomicUsize>,
        amounts: &[f32],
    ) {
        for &amount in amounts {
            tx.send(Transaction::new(
                counter.fetch_add(1, Ordering::SeqCst),
                amount,
            ))
            .unwrap();
        }
    }

    let handle1 = std::thread::spawn(move || {
        send_transactions(tx1, counter1, &[1.0, 3.0, 5.0]);
    });

    let counter2 = Arc::clone(&counter);
    let handle2 = std::thread::spawn(move || {
        send_transactions(tx, counter2, &[-2.0, -4.0, 6.0]);
    });

    std::thread::spawn(move || {
        let mut balance = 0.0;
        let mut event_log = Vec::new(); // Event log to store all transactions
        for received in rx {
            balance += received.amount;
            event_log.push(received); // Store the event
            println!(
                "Transaction {}: amount {}, balance: {}",
                event_log.last().unwrap().id,
                event_log.last().unwrap().amount,
                balance
            );
        }

        println!("Total: {}", balance);
        println!("Event log:");
        for event in event_log {
            println!("Transaction {}: amount {}", event.id, event.amount);
        }
    })
    .join()
    .unwrap();

    handle1.join().unwrap();
    handle2.join().unwrap();
}
